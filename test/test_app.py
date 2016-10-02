from flask import Flask, g, request, url_for, jsonify
from functools import wraps

import time

app_under_test = Flask(__name__)


def monitor(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print "Monitored"#, f.__name__
        return f()
    return decorated_function

@app_under_test.before_request
def before_request():
    g.start = time.time()


@app_under_test.after_request
def after_request(response):
    diff = int((time.time() - g.start) * 1000)  # to get a time in ms
    print request.endpoint, "took", diff, "ms to run"
    return response

@app_under_test.route("/")
@monitor
def index():
    return "Hello World!"


@app_under_test.route("/long_running_endpoint")
@monitor
def long_running_endpoint():
    time.sleep(3)
    return "Hello World!"

@app_under_test.route("/list_routes")
def list_routes():
    import urllib
    output = []
    for rule in app_under_test.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    print output
    return jsonify(output)


if __name__ == "__main__":
    app_under_test.run(debug=True)