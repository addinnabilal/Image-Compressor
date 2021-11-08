import os
import compress
from flask import Flask, flash, request, redirect, url_for, session
import logging
import flask_cors
from werkzeug.utils import secure_filename



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'storage'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def handleFileUpload():
    target=os.path.join(UPLOAD_FOLDER,'uploaded')
    if not os.path.isdir(target):
        os.mkdir(target)
    logger.info("Handling file upload..")
    file = request.files['file']
    k = int(request.form['k'])
    logger.info(k)
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    file.save(destination)
    session['uploadFilePath']=destination
    response = compress.compress_function(k, file.filename)
    return response

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig(logging.conf)
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')