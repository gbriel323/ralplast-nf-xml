from flask import Flask
from upload.upload_handler import app as upload_app
import awsgi

app = Flask(__name__)
app.register_blueprint(upload_app)


def handler(event, context):
    return awsgi.response(app, event, context)
