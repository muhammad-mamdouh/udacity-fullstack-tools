from flask import Flask, jsonify, request, url_for, abort, g
from flask_httpauth import HTTPBasicAuth
from models import Base, User
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///users.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    else:
        g.user = user
        return True


@app.route('/api/users', methods=['POST'])
def new_user():
    request_data = request.json
    username = request_data['username']
    password = request_data['password']

    if username is None or password is None:
        abort(400)    # Missing arguments
    elif session.query(User).filter_by(username=username).first() is not None:
        print("existing user")
        return jsonify({'message': 'user already exists'}), 200

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


@app.route('/api/protected_resource')
@auth.login_required
def get_resource():
    return jsonify({ 'data': f'Hello, {g.user.username}!' })


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
