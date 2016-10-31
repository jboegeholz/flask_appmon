import urllib2
from flask import request, render_template, jsonify, Blueprint
from appmon.forms import ApplicationForm
from flask import abort
from appmon.frontend.models import HitCount

data = {}

frontend = Blueprint('frontend', __name__)

@frontend.route("/register_app", methods=["POST", "GET"])
def register_app():
    form = ApplicationForm(request.form)
    if request.method == 'POST' and form.validate():

        pass
    return render_template("register_app.html", form=form)

@frontend.route("/get_routes", methods=["GET"])
def get_routes():
    response = urllib2.urlopen("http://" + data["port"] + "/list_routes")
    if response.msg == "OK":
        print response.read()

    return "Ok"

@frontend.route("/receive_data", methods=["POST"])
def receive_data():
    """
    Receives the data from the app under monitoring
    :return:
    """
    if "app" not in request.form or "endpoint" not in request.form:
        abort(404)

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

@frontend.route("/_get_hit_count", methods=["GET"])
def get_hit_count():
    print "get_hit_count"
    args = request.args
    print args
    # hit_count = data[args["app"]][args["endpoint"]]["hit_count"]
    hit_count = HitCount.query().filter(app=args["app"]).filter(endpoint=args["endpoint"]).one()
    return jsonify(hit_count=hit_count)

@frontend.route("/hit_count")
def hit_count():
    return render_template("show_hit_count.html")
