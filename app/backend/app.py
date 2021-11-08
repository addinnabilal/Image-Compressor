from flask import Flask
from flask.wrappers import Request
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Start")



app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def handleFileUpload():
    pass