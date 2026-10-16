import os

from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from sqlalchemy import URL

db = SQLAlchemy()
csrf = CSRFProtect()


def create_app(test_config=None):
    load_dotenv()
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    config_overrides = test_config or {}
    database_url = config_overrides.get("SQLALCHEMY_DATABASE_URI") or os.getenv(
        "databaseUrl"
    )
    secret_key = os.getenv("secretKey") or config_overrides.get("SECRET_KEY")

    if not secret_key:
        raise RuntimeError("Set secretKey in the environment or .env file.")
    if not database_url and not os.getenv("dbPassword"):
        raise RuntimeError("Set dbPassword or databaseUrl in the environment or .env file.")

    app.config.from_mapping(
        SECRET_KEY=secret_key,
        SQLALCHEMY_DATABASE_URI=database_url
        or URL.create(
            "mysql+pymysql",
            username=os.getenv("dbUser", "warehouse"),
            password=os.getenv("dbPassword"),
            host=os.getenv("dbHost", "localhost"),
            port=int(os.getenv("dbPort", "3306")),
            database=os.getenv("dbName", "warehouse"),
        ),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )
    app.config.update(config_overrides)

    db.init_app(app)
    csrf.init_app(app)

    from app import routes

    app.register_blueprint(routes.bp)

    with app.app_context():
        db.create_all()

    return app
