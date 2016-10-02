import urllib2
import json
from flask import Flask, request

app_mon = Flask(__name__)

aut = {}

@app_mon.route("/register_app", methods=["POST"])
def register_app():
    print request.form["app_name"]
    print request.form["port"]
    aut["app_name"] = request.form["app_name"]
    aut["port"] = request.form["port"]
    return "Ok"

@app_mon.route("/get_routes", methods=["GET"])
def get_routes():
    response = urllib2.urlopen("http://" + aut["port"] + "/list_routes")
    if response.msg == "OK":
        print response.read()

    return "Ok"

if __name__ == '__main__':
    app_mon.run(port=8080)
