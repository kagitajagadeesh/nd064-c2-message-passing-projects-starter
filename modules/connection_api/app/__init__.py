import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
# from kafka import KafkaProducer

db = SQLAlchemy()

# TOPIC_NAME = 'locations'
# KAFKA_SERVER = os.environ.get("KAFKA_URI", "kafka:9092")
# producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)

def create_app(env=None):
    from app.config import config_by_name
    from app.routes import register_routes

    app = Flask(__name__)
    app.config.from_object(config_by_name[env or "test"])
    # app.config.from_mapping(
    #     # FLASK_ENV= 'development',
    #     DEBUG = True,
    #     SQLALCHEMY_DATABASE_URI= 'postgresql://ct_admin:d293aW1zb3NlY3VyZQ==@host.docker.internal:5432/geoconnections',
    #     SQLALCHEMY_TRACK_MODIFICATIONS=False
    # )
    # print(app.config)
    api = Api(app, title="UdaConnect API", version="0.1.0")

    CORS(app)  # Set CORS for development

    register_routes(api, app)
    db.init_app(app)

    @app.route("/health")
    def health():
        return jsonify("healthy")

    return app
