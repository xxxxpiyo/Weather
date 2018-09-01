from flask import Flask, request, jsonify, Response
import json
import datetime
app = Flask(__name__)

localFile = "./data/today.json"

@app.route('/weather/input', methods=['POST'])
def DataCollecter():
    if request.method == "POST":
        return inputPost(request)

    else:
        return ("aho",405)

@app.route('/weather/today', methods=['GET'])
def today():
    f = open(localFile, "r")
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
    writeToday(json.dumps(postData))

    return ("OK",200)

def writeToday(j):
    f = open(localFile, 'w')
    f.write(j)
    f.close()

def postGCPDataStore(j):
    pass

def jsonp(data, callback="function"):
    return Response(
        "%s(%s);" %(callback, json.dumps(data)),
        mimetype="text/javascript"
        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
