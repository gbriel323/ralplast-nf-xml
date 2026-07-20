from flask import Flask
from upload.upload_handler import upload_bp
import awsgi

app = Flask(__name__)

app.register_blueprint(upload_bp)


def handler(event, context):
    return awsgi.response(app, event, context)