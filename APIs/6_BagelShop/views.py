from flask import Flask, jsonify, request, abort, g
from flask_httpauth import HTTPBasicAuth
from models import Base, User, Bagel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


engine = create_engine('sqlite:///bagelShop.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

app = Flask(__name__)
auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = session.query(User).filter_by(username=username).first()
    if not user:
        print('User not found!')
        return False
    elif not user.verify_password(password):
        print('Unable to verify password')
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
        print('Missing arguments')
        abort(400)
    elif session.query(User).filter_by(username=username).first() is not None:
        print("existing user")
        return jsonify({'message': 'user already exists'}), 200
    else:
        user = User(username=username)
        user.hash_password(password)
        session.add(user)
        session.commit()
        return jsonify({ 'username': user.username }), 201


@app.route('/api/bagels', methods = ['GET','POST'])
@auth.login_required
def showAllBagels():
    if request.method == 'GET':
        bagels = session.query(Bagel).all()
        return jsonify(bagels = [bagel.serialize for bagel in bagels])
    elif request.method == 'POST':
        request_data = request.json
        name = request_data['name']
        description = request_data['description']
        picture = request_data['picture']
        price = request_data['price']
        new_bagel = Bagel(name=name, description=description, picture=picture, price=price)
        session.add(new_bagel)
        session.commit()
        return jsonify(new_bagel.serialize)


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
