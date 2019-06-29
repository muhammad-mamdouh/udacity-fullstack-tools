#!/usr/bin/env python3
#
from flask import Flask, render_template, url_for, request, redirect, flash
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/index')
def welcome():
    return "Welcome to our Flask Application."


@app.route('/restaurants/')
def list_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('RestaurantsList.html', restaurants_list=restaurants)


@app.route('/restaurants/<int:restaurant_id>/menu/')
def restaurant_items(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('RestaurantMenu.html',
                           restaurant=restaurant, items=items)


@app.route('/restaurants/<int:restaurant_id>/new',
           methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'],
                            restaurant_id=restaurant_id)
        session.add(new_item)
        session.commit()
        flash("New Menu Item Created!")
        return redirect(url_for('restaurant_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('NewMenuItem.html',
                               restaurant_id=restaurant_id)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit/',
           methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item_to_edit = session.query(MenuItem).filter_by(id=menu_id).first()
    if request.method == 'POST':
        item_to_edit.name = request.form['name']
        session.add(item_to_edit)
        session.commit()
        flash("Menu Item Edited Successfully!")
        return redirect(url_for('restaurant_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('EditMenuItem.html',
                               restaurant_id=restaurant_id,
                               menu_id=menu_id, item=item_to_edit)


@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/',
           methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("Menu Item Deleted Successfully!")
        return redirect(url_for('restaurant_items',
                                restaurant_id=restaurant_id))
    else:
        return render_template('DeleteMenuItem.html', item=item_to_delete)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
