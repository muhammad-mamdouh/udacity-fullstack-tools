# Use an ORM(SQLAlchemy) to create a database and execute CRUD operations on it. 

## Install SQLAlchemy from your shell(Unix-Based)
1. First step, you should intall the MySql,like these:
```
sudo apt-get install mysql-server
sudo apt-get install mysql-client
sudo apt-get install libmysqlclient15-dev
```

2. Second step, install the python-mysqldb:
```
sudo apt-get install python-mysqldb
```

3. Third step, install the easy_install:
```
sudo wget http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py
```

4. Forth step, install the MySQL-Python:
```
sudo easy_install MySQL-Python
```

5. Finally, install sqlalchemy:
```
sudo easy_install SQLAlchemy
```

### Running `DatabaseSetup.py` script will give you a new database file `restaurantmenu.db`
```
python3 DatabaseSetup.py
```

### Now let's populate our `restaurantmenu.db` SQLite database with some information
We'll perform all of the CRUD operations with SQLAlchemy on our database by
running `DbPopulate.py` script
