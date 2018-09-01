from flask import Flask, request
import json
import datetime
app = Flask(__name__)

@app.route('/weather/input', methods=['POST',"GET"])
def DataCollecter():
    if request.method == "POST":
        postKey = ['id','temperature','pressure','humidity']
        postData = {}
        app.logger.debug(request.method)
        app.logger.debug(request.headers)
        app.logger.debug(request.form)
        if request.method == 'POST':
        if not 'key' in request.form.keys()  and not request.form['key'].equals('piyopiyo'):
          return "aho!"

        today = datetime.datetime.today()
        for key in postKey:
         postData[key] = request.form[key] if key in request.form.keys() else None

        postData.update(
          date=today.strftime("%Y/%m/%d"),
          time=today.strftime("%H:%M:%S")
        )

        app.logger.debug(json.dumps(postData))

        return 'aaa'
    else if request.method == "GET":
        return "GETS!"

    else:
        return "aho"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
