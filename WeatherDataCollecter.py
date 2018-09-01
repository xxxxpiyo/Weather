from flask import Flask, request
import json
import datetime
app = Flask(__name__)

@app.route('/weather/input', methods=['POST'])
def DataCollecter():
    if request.method == "POST":
        return post(request)

    else:
        return ("aho",405)

def post(r):
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
      date=today.strftime("%Y/%m/%d"),
      time=today.strftime("%H:%M:%S")
    )
    app.logger.debug(json.dumps(postData))

    return ("OK",200)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
