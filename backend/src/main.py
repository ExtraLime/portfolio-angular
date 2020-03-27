from __future__ import absolute_import

from flask import Flask, jsonify, request
from flask_cors import CORS

from .entities.entity import Session, engine, Base
from .entities.exam import Project, ExamSchema

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


