import urllib2
import json
from flask import Flask, request, render_template, jsonify
from Application import Application

app_mon = Flask(__name__)

data = {}

@app_mon.route("/register_app", methods=["POST", "GET"])
def register_app():
    form = Application(request.form)
    if request.method == 'POST' and form.validate():

        pass
    return render_template("register_app.html", form=form)

@app_mon.route("/get_routes", methods=["GET"])
def get_routes():
    response = urllib2.urlopen("http://" + data["port"] + "/list_routes")
    if response.msg == "OK":
        print response.read()

    return "Ok"

@app_mon.route("/receive_data", methods=["POST"])
def receive_data():
    """
    Receives the data from the app under monitoring
    :return:
    """
    app = request.form["app"]
    endpoint = request.form["endpoint"]
    timestamp = request.form["timestamp"]
    type = request.form["type"]
    print app, endpoint, type, timestamp

    if app not in data:
        data[app] = {}

    if endpoint not in data[app]:
        data[app][endpoint] = {"hit_count": 0}
    if type == "start":
        data[app][endpoint]["hit_count"] += 1
    return "Ok"

@app_mon.route("/get_hit_count", methods=["GET"])
def get_hit_count():
    print "get_hit_count"
    args = request.args
    print args
    hit_count = data[args["app"]][args["endpoint"]]["hit_count"]
    return jsonify(hit_count=hit_count)

if __name__ == '__main__':
    app_mon.run(port=8080)
