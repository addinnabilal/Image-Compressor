import os
import compress
from flask import Flask, flash, request, redirect, url_for, session, send_file
import logging
import flask_cors
from werkzeug.utils import secure_filename
from flask.json import jsonify

currentData = {'diff': 0, 'time': 0}
# currentK = 5

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

UPLOAD_FOLDER = 'storage'
DOWNLOAD_FOLDER = 'storage/compressed/'

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def hello():
    return "Hello, World!"

@app.route('/upload', methods=['POST'])
def handleFileUpload():
    if not os.path.isdir(UPLOAD_FOLDER):
        os.mkdir(UPLOAD_FOLDER)
    target=os.path.join(UPLOAD_FOLDER,'uploaded')
    logger.info("Handling file upload..")
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files['file']
    filename = secure_filename(file.filename)
    destination="/".join([target, filename])
    if os.path.exists(destination):
        logger.info("Duplicate file. Deleting older file.")
        os.remove(destination)
    file.save(destination)
    session['uploadFilePath']=destination
    
    return currentData

@app.route('/data')
def getCurrentData():
    global currentData
    logger.info(currentData)
    return currentData

# @app.route('/k', methods=['POST'])
# def setK():
#     global currentK
#     currentK = int(request.form['k'])
#     logger.info(currentK)
#     return "Set K success"

@app.route('/compress/<k>_<filename>', methods=['GET'])
def download(filename, k):
    # TODO : Delete after done
    global currentData
    currentData = compress.compress_function(int(k), filename)
    logger.info(currentData)
    logger.info("Handling download..")
    compressed_path = DOWNLOAD_FOLDER + "compressed" + "_" + str(k) + "_" + filename
    return send_file(compressed_path, as_attachment=True)

if __name__ == "__main__":
    import logging.config
    logging.config.fileConfig(logging.conf)
    app.secret_key = os.urandom(24)
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True,host="0.0.0.0",use_reloader=False)

flask_cors.CORS(app, expose_headers='Authorization')