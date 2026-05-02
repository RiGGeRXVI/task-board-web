from flask import Flask
from .db import close_db, init_db_command
from .routes import bp


def create_app():
    app = Flask(__name__)
    app.config["DATABASE"] = "database.db"

    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.register_blueprint(bp)

    return app