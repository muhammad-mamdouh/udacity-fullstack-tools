#!/usr/bin/env python3
#
from flask import Flask, render_template, url_for
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db', connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def welcome():
    return "Welcome to our Flask Application."


@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_items(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/')
def edit_restaurant_item(restaurant_id, menu_id):
    return "restaurant_id:{}  >>  menu_id:{}".format(str(restaurant_id), str(menu_id))


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/')
def delete_restaurant_item(restaurant_id, menu_id):
    return "restaurant_id:{}  >>  menu_id:{}".format(str(restaurant_id), str(menu_id))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
