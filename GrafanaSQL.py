# '''
# / should return 200 ok. Used for "Test connection" on the datasource config page.
# /search used by the find metric options on the query tab in panels.
# /query should return metrics based on input.
# /annotations should return annotations.
# '''
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./test.db'
db = SQLAlchemy(app)

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
    # query?db=test&epoch=ms&q=SELECT mean("value") FROM "it" WHERE time > 1456786800s and time < 1456790400s GROUP BY time(360s) fill(null)
    print("db: %s" %(request.args.get('db')))
    print("epoch: %s" %(request.args.get('epoch')))
    print("query: %s" %(request.args.get('q')))
    sql = request.args.get('q')
    conn = db.engine.connect() # get a mysql connection
    print
    rs = conn.execute(sql).fetchall()
    print "---------------"
    print rs
    print "---------------"
    return '''
{"results":[{"series":[{"name":"it","columns":["time","mean"],"values":[[1456786800000,12.433333333333332],[1456787160000,12.4],[1456787520000,12.433333333333332],[1456787880000,12.4],[1456788240000,12.4],[1456788600000,12.4],[1456788960000,12.4],[1456789320000,12.4],[1456789680000,12.4],[1456790040000,12.4]]}]}]}  '''

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)