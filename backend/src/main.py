from __future__ import absolute_import
from entities.entity import Session, engine, Base
from entities.exam import Project

Base.metadata.create_all(engine)

session = Session()

projects = session.query(Project).all()

if len(projects) == 0:
    python_project = Project('PDXcrimemap.net','Visualize live crime in PDX','script')

    session.add(python_project)
    session.commit()
    session.close()

    projects = session.query(Project).all()

print('### Projects:')
for project in projects:
    print(f'{project.id} {project.description}')