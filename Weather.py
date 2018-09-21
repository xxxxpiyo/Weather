# coding=utf-8
from flask import Flask, request, jsonify, Response
import json
import datetime
import os
import ConnectGCP

app = Flask(__name__)
IDs = [1,2]
gcp_config_ini = os.path.dirname(__file__) + "/config.ini"
localFile = os.path.dirname(__file__) + "/data/today_%s.json"

@app.route('/weather/input', methods=['POST'])
def DataCollecter():
    if request.method == "POST":
        return inputPost(request)

    else:
        return ("aho",405)

@app.route('/weather/today/<id>', methods=['GET'])
def today(id):
    flag = False
    for i in IDs:
        if i == int(id):
            flag = True
            break
    if flag != True:
        return ("aho", 405)

    f = open(localFile % (id), "r")
    callback = request.args.get('callback')
    return jsonp(json.load(f), callback)


def inputPost(r):
    postKey = ['id','temperature','pressure','humidity']
    app.logger.debug(request.method)
    app.logger.debug(request.headers)
    app.logger.debug(request.json)
    app.logger.debug(type(request.json))
    postData = {}

    if not 'key' in request.json.keys()  and not request.json['key'].equals('piyopiyo'):
      return "aho!"

    today = datetime.datetime.today()
    for key in postKey:
     postData[key] = request.json[key] if key in request.json.keys() else None

    postData.update(
      datetime=today.strftime("%Y/%m/%d %H:%M:%S"),
    )
    app.logger.debug(json.dumps(postData))
    writeToday(json.dumps(postData),postData["id"])
    postData.pop("datetime")
    postGCPDataStore(postData)

    return ("OK",200)

def writeToday(j, id):
    f = open(localFile % (id), 'w')
    f.write(j)
    f.close()

def postGCPDataStore(j):
    gcp = ConnectGCP.ConnectGCP(gcp_config_ini)
    gcp.connectDS()
    gcp.postData(j)

def jsonp(data, callback="function"):
    return Response(
        "%s(%s);" %(callback, json.dumps(data)),
        mimetype="text/javascript"
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
