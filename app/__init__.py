from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.mqtt_broker import init_broker
from app.config import Config

db = SQLAlchemy()
mqtt_client = init_broker()
app = Flask(__name__)
def create_app():
    app.config.from_object(Config)
    db.init_app(app)

    # Register blueprints
    from app.routes import routes as routes_blueprint
    app.register_blueprint(routes_blueprint)

    return app
