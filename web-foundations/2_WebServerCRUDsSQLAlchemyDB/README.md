# Data Driven Web Application

This is a simple data driven web application that interacts with SQLAlchemy(ORM)
database and makes it possible to receive GET and POST requests.

### Available resources
```
# The root path
GET
localhost:8000/

# Display all of the restaurants
GET
localhost:8000/restaurants

# Make a new restaurant
GET && POST
localhost:8000/restaurant/new

# Update an existing restaurant
GET && POST 
localhost:8000/restaurant/restaurant_id/edit

# Delete an existing restaurant
GET && POST
localhost:8000/restaurant/restaurant_id/delete
```
