from flask import Flask
from extensions import db


def create_app(config=None, app_name="flask_appmon"):

    app = Flask(app_name)
    app.config["SQLALCHEMY_DATABASE_URI"] = "'sqlite:///app.db'"
    # configure_app(app, config)
    # configure_hook(app)
    configure_blueprints(app)
    configure_extensions(app)
    # configure_logging(app)
    # configure_template_filters(app)
    # configure_error_handlers(app)
    # configure_cli(app)

    return app

def configure_extensions(app):
    db.init_app(app)



def configure_blueprints(app):
    from frontend import frontend
    app.register_blueprint(frontend)