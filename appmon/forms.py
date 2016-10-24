from wtforms import Form, StringField


class ApplicationForm(Form):
    app_name = StringField("Application Name")
    client = StringField("Client")
    port = StringField("Port")