"""
This script performs different CRUD operations on
the restaurantmenu.db database
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from DatabaseSetup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind = engine)
session = DBSession()


def get_all_restaurants():
    try:
        restaurants_list = []
        restaurants_obj = session.query(Restaurant).all()
        for restaurant in restaurants_obj:
            restaurants_list.append(restaurant.name)
        return restaurants_list
    except:
        return "Operation Failed!"


def create_new_restaurant(restaurant_name):
    try:
        restaurant_obj = Restaurant(name = restaurant_name)
        session.add(restaurant_obj)
        session.commit()
        return True
    except:
        return "Operation Failed!"


def edit_restaurant_name(old_id, new_name):
    try:
        restaurant_obj = session.query(Restaurant).filter_by(id = old_id).one()
        restaurant_obj.name = new_name
        session.add(restaurant_obj)
        session.commit()
        return True
    except:
        return "Operation Failed!"


def delete_restaurant(rest_id):
    try:
        restaurant_obj = session.query(Restaurant).filter_by(id = rest_id).one()
        session.delete(restaurant_obj)
        session.commit()
        return True
    except:
        return "Operation Failed!"


def get_restaurant_id_by_name(restaurant_name):
    try:
        restaurant_obj = session.query(Restaurant).filter_by(name = restaurant_name)
        for item in restaurant_obj:
            restaurant_id = item.id
        return restaurant_id
    except:
        return "Operation Failed!"


def get_restaurant_name_by_id(restaurant_id):
    try:
        restaurant_obj = session.query(Restaurant).filter_by(id = restaurant_id)
        for item in restaurant_obj:
            restaurant_name = item.name
        return restaurant_name
    except:
        return "Operation Failed!"
