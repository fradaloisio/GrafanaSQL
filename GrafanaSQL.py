# '''
# / should return 200 ok. Used for "Test connection" on the datasource config page.
# /search used by the find metric options on the query tab in panels.
# /query should return metrics based on input.
# /annotations should return annotations.
# '''
import json, re, time, datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dateutil.parser import parse

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+pg8000://user@127.0.0.1:5432/mySpecialDB'
db = SQLAlchemy(app)
conn = db.engine.connect()

if conn != None:
    print "Connected"
else:
    print "NOT Connected"
    exit()


#/ should return 200 ok. Used for "Test connection" on the datasource config page.
@app.route('/')
def test_connection():
    return "GrafanSQL here!", 200

#/search used by the find metric options on the query tab in panels.
@app.route('/search')
def search():
    tables = db.engine.table_names()
    return str(tables)

# /query should return metrics based on input.
@app.route('/query')
def query():
    # Grafana:
    # select timestamp as time,value from measurements where measure == 'ot' AND timerange($timeFilter,'%Y-%m-%d %H:%M:%S')
    response = []
    results = []
    result = {}

    # query?db=test&epoch=ms&q=SELECT mean("value") FROM "it" WHERE time > 1456786800s and time < 1456790400s GROUP BY time(360s) fill(null)
    print("db: %s" %(request.args.get('db')))
    db = request.args.get('db')
    epoch = request.args.get('epoch')
    print("epoch: %s" %(request.args.get('epoch')))
    print("query: %s" %(request.args.get('q')))
    sql = request.args.get('q')

    for query in sql.split("\n"):
        print query
        series = []
        serie = {}
        values = []

        serie["name"] = db # TODO: assign the right value
        serie["columns"]= ["time","value"]
        if sql != "SHOW MEASUREMENTS":
            timerange = re.search('timerange\(time.?..?(.*?)s and time.?..?(.*?)s.?,.?\'(.*?)\'\)', query).group(1,2,3)
            if timerange:
                t1 = time.strftime(timerange[2], time.gmtime(int(timerange[0])))
                t2 = time.strftime(timerange[2], time.gmtime(int(timerange[1])))
                query = query.replace("timerange(", "")
                query = query.replace("%ss" % timerange[0], "'%s'" % t1)
                query = re.sub("%ss.?,.?\'%s\'\)" % (timerange[1], timerange[2]), "'%s'" % t2, query)

                q = conn.execute(query)
                rs = q.fetchall()

                serie["columns"] = q.keys()

                for r in rs:
                    result_array = []
                    if isinstance(r[0], datetime.datetime):
                        t = int(r[0].strftime('%s')) * 1000 if epoch == "ms" else int(r[0].strftime('%s'))
                    else:
                        t = int(parse(r[0]).strftime('%s')) * 1000 if epoch == "ms" else int(parse(r[0]).strftime('%s'))
                    result_array.append(t)

                    for v in range(1,r.__len__()):
                        result_array.append(r[v])
                    values.append(result_array)

        elif sql == "SHOW MEASUREMENTS":
            serie["columns"] = ["name"]
            tables = db.engine.table_names()
            values.append(tables)
            
        elif sql == "SHOW TAG KEYS FROM":
            #TODO Show columns name
            pass

        serie["values"] = values
        series.append(serie)
        results.append({"series": series})

    response = {"results":results}
    #print json.dumps(response)
    return json.dumps(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
