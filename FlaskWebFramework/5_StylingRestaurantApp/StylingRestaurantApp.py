#!/usr/bin/env python3
#
from flask import Flask, render_template, url_for, request, redirect, flash, jsonify
from DatabaseSetup import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db',
                       connect_args={'check_same_thread': False})
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/')
@app.route('/restaurants/')
def show_restaurants():
    restaurants = session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants,
                           title='All Restaurants', header='Restaurants')


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def new_restaurant():
    if request.method == 'POST':
        new_restaurant = Restaurant(name=request.form['name'])
        session.add(new_restaurant)
        session.commit()
        flash("New restaurant has been opened successfully!", "success")
        return redirect(url_for('show_restaurants'))
    else:
        return render_template('new-restaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    restaurant_to_edit = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == 'POST':
        if request.form['name']:
            restaurant_to_edit.name = request.form['name']
        session.add(restaurant_to_edit)
        session.commit()
        flash("Restaurant has been edited successfully!", "success")
        return redirect(url_for('show_restaurant_menus', restaurant_id=restaurant_to_edit.id))
    else:
        return render_template('edit-restaurant.html', restaurant=restaurant_to_edit)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    restaurant_to_delete = session.query(Restaurant).filter_by(id=restaurant_id).first()
    if request.method == 'POST':
        session.delete(restaurant_to_delete)
        session.commit()
        flash("Restaurant has been deleted successfully!", "success")
        return redirect(url_for('show_restaurants'))
    return render_template('delete-restaurant.html', restaurant_id=restaurant_to_delete.id)


@app.route('/restaurant/<int:restaurant_id>/menu/')
def show_restaurant_menus(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return render_template('restaurant-menu.html', restaurant=restaurant,
                           menu_items=menu_items, title=f'{restaurant.name.capitalize()} Menu Items',
                           header=f'{restaurant.name.capitalize()} Restaurant Menu Items')


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def new_menu_item(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        new_item = MenuItem(name=request.form['name'], description=request.form['description'],
                            price=request.form['price'], course=request.form['course'],
                            restaurant_id=restaurant.id)
        session.add(new_item)
        session.commit()
        flash("New menu item has been successfully added!", "success")
        return redirect(url_for('show_restaurant_menus',
                                restaurant_id=restaurant.id))
    else:
        return render_template('new-item.html', restaurant_id=restaurant.id,
                               title='Add New Item', header='Add New Menu Item',
                               action_btn='Add')


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_id):
    item_to_edit = session.query(MenuItem).filter_by(id=menu_id).first()
    if request.method == 'POST':
        if request.form['name']:
            item_to_edit.name = request.form['name']
        if request.form['description']:
            item_to_edit.description = request.form['description']
        if request.form['price']:
            item_to_edit.price = request.form['price']
        if request.form['course']:
            item_to_edit.course = request.form['course']
            print(request.form['course'])
        session.add(item_to_edit)
        session.commit()
        flash("Menu item has been updated successfully!", "success")
        return redirect(url_for('show_restaurant_menus',
                                restaurant_id=restaurant_id))
    else:
        return render_template('edit-item.html', restaurant_id=restaurant_id, item=item_to_edit,
                               title='Edit New Item', header='Edit Menu Item',
                               action_btn='Update')


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_id):
    item_to_delete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(item_to_delete)
        session.commit()
        flash("Menu item has been deleted successfully!", "success")
        return redirect(url_for('show_restaurant_menus',
                                restaurant_id=restaurant_id))
    else:
        return render_template('delete-item.html', restaurant_id=restaurant_id, menu_id=item_to_delete.id)


# Making an API Endpoint (GET Request)
@app.route('/restaurant/<int:restaurant_id>/menu/JSON/')
def restaurant_menu_JSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id).all()
    return jsonify(MenuItem=[item.serialize for item in items])


# Making an API Endpoint (GET Request)
@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def restaurant_specific_menu_JSON(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu_item.serialize)


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
