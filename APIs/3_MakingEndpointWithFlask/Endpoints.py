from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Puppy

engine = create_engine('sqlite:///puppies.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route("/")
@app.route("/puppies/", methods=['GET', 'POST'])
def puppiesFunction():
    if request.method == 'GET':
        return get_all_puppies()
    elif request.method == 'POST':
        return make_new_puppy()


@app.route("/puppies/<int:id>", methods=['GET', 'PUT', 'DELETE'])
def puppiesFunctionId(id):
    if request.method == 'GET':
        return get_puppy(id)
    elif request.method == 'PUT':
        return update_puppy(id)
    elif request.method == 'DELETE':
        return delete_puppy(id)


def get_all_puppies():
    puppies = session.query(Puppy).all()
    return jsonify(Puppies=[i.serialize for i in puppies])


def get_puppy(id):
    puppy = session.query(Puppy).filter_by(id=id).one()
    return jsonify(Puppy=puppy.serialize)


def make_new_puppy(name, description):
    puppy = Puppy(name=name, description=description)
    session.add(puppy)
    session.commit()
    return jsonify(Puppy=puppy.serialize)


def update_puppy(id, name, description):
    puppy = session.query(Puppy).filter_by(id=id).one()
    if name:
        puppy.name = name
    if description:
        puppy.description = description
    session.add(puppy)
    session.commit()
    return f"Updated a Puppy with id: {id}"


def delete_puppy(id):
    puppy = session.query(Puppy).filter_by(id=id).one()
    session.delete(puppy)
    session.commit()
    return f"Removed Puppy with id: {id}"


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
