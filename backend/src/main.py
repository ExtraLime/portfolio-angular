from __future__ import absolute_import
import os
import flask
from flask import Flask, flash, jsonify, request, redirect, url_for
from flask_cors import CORS
from shelljob import proc
import psycopg2

from .entities.entity import Session, engine, Base
from .entities.exam import Project, ExamSchema
from .entities.log_entry import LogEntry, LogSchema
from .log_entry.process_log import process_log

from .auth import AuthError, requires_auth

from werkzeug.utils import secure_filename

#create app
app = Flask(__name__)
#cross-origin
CORS(app)


Base.metadata.create_all(engine)

@app.route('/projects')

def get_projects():
    #start sessions
    session = Session()
    #fetch all data
    proj_obs = session.query(Project).all()
    #transform to be json-readable
    schema = ExamSchema(many=True)
    projects = schema.dump(proj_obs)

    #serialize as JSON
    session.close()

    return jsonify(projects)


@app.route('/projects', methods=['POST'])
@requires_auth
def add_project():

    posted_proj = ExamSchema(only=('title','description'))\
        .load(request.get_json())

    project = Project(**posted_proj, created_by='HTTP post request')

    session = Session()
    session.add(project)

    session.commit()

    new_project = ExamSchema().dump(project)
    session.close()

    return jsonify(new_project), 201

@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

UPLOAD_FOLDER = 'src/files'
ALLOWED_EXTENSIONS = {'txt', 'json', 'log','log.1'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/fileupload', methods=["GET",'POST'])
def uploaded():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            full_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(full_path)
            return '''File has been uploaded'''
    
    return '<div class="return1" style="margin-top:15px;"><h3>There was a problem. Check the extension and try again</h3> </div>'

@app.route('/process', methods=["GET",'POST'])

def process_file():
    if request.method == "POST":
        file = request.files['file']
        filename = file.filename + '_processed'
        full_path = os.path.join('src/processed', filename)
        file.save(full_path)
        process_log(full_path)
    return '''<html><p>"You Processed a file </p></html>'''

@app.route('/explore', methods=['GET'])

def get_processed_files():
    return os.listdir(os.getcwd()+'/src/processed')

@app.route( '/stream' )
def stream():
    g = proc.Group()
    p = g.run( [ "bash", "-c", "for ((i=0;i<100;i=i+1)); do echo $i; sleep 1; done" ] )

    def read_process():
        while g.is_pending():
            lines = g.readlines()
            for proc, line in lines:
                yield line

    return flask.Response( read_process(), mimetype= 'text/plain' )

@app.route('/mapData')

def get_map_data():
    #start sessions
    session = Session()
    #fetch all data
    points = session.execute("""SELECT ip, lat, lng FROM log_entry""")
    #transform to be json-readable
    
    

    #serialize as JSON
    session.close()

    return jsonify({'result': [dict(row) for row in points]})
