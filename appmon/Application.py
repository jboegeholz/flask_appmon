from wtforms import Form, StringField


class Application(Form):
    app_name = StringField("Application Name")
    client = StringField("Client")
    port = StringField("Port")