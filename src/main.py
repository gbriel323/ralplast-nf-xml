from flask import Flask
from .upload.upload_handler import app as upload_app

app = Flask(__name__)
app.register_blueprint(upload_app)
