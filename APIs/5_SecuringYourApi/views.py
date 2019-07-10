from flask import Flask, jsonify, request, url_for, abort
from models import Base, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///users.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)


@app.route('/api/users', methods=['POST'])
def new_user():
    request_data = request.json
    username = request_data['username']
    password = request_data['password']

    if username is None or password is None:
        abort(400)    # Missing arguments
    elif session.query(User).filter_by(username=username).first() is not None:
        return jsonify({'username': username}), 201     # Already existing user
    user = User(username=username)
    user.hash_password(password)
    session.add(user)
    session.commit()

    return jsonify({ 'username': user.username }), 201,\
           {'Location': url_for('get_user', id = user.id, _external = True)}


@app.route('/api/users/<int:user_id>')
def get_user(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    if not user:
        abort(400)
    return jsonify({'username': user.username})


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
