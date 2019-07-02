#
# Configuration Code
# Column, ForeignKey, Integer and String Classes will be used when we're
#   writing our mapper code
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# used in creating our foreign key relationships at the mapper code
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# The declarative_base() class will let SQLAlchemy know that our classes are
#    special SQLAlchemy classes that correspond to tables in our databases
Base = declarative_base()


# Restaurant-Table code representation and Mapper code
class Restaurant(Base):
    __tablename__ = 'restaurant'

    # Mapper Code
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


# MenuItem-Table code representation and Mapper code
class MenuItem(Base):
    __tablename__ = 'menu_item'

    # Mapper Code
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    # This method will help define what data we want to send across
    @property
    def serialize(self):
        '''Returns object data in easily serializable format'''
        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }


# Create the engine, the starting point for any SQLAlchemy app.
engine = create_engine('sqlite:///restaurantmenu.db')

# goes into the db and adds the classes we've created as new tables in it
Base.metadata.create_all(engine)
