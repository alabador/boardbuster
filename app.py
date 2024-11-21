# from flask import Flask, render_template, json, redirect
# from flask_mysqldb import MySQL
# from flask import request
# import os

# app = Flask(__name__)

# app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
# app.config['MYSQL_USER'] = 'cs340_labadora'
# app.config['MYSQL_PASSWORD'] = '7708' #last 4 of onid
# app.config['MYSQL_DB'] = 'cs340_labadora'
# app.config['MYSQL_CURSORCLASS'] = "DictCursor"


# mysql = MySQL(app)


# # Routes
# @app.route('/')
# def root():
#     query = "SELECT * FROM diagnostic;"
#     query1 = 'DROP TABLE IF EXISTS diagnostic;';
#     query2 = 'CREATE TABLE diagnostic(id INT PRIMARY KEY AUTO_INCREMENT, text VARCHAR(255) NOT NULL);';
#     query3 = 'INSERT INTO diagnostic (text) VALUES ("MySQL is working for yourONID!")';
#     query4 = 'SELECT * FROM diagnostic;';
#     cur = mysql.connection.cursor()
#     cur.execute(query1)
#     cur.execute(query2)
#     cur.execute(query3)
#     cur.execute(query4)
#     results = cur.fetchall()

#     return "<h1>MySQL Results</h1>" + str(results[0])


# # Listener
# if __name__ == "__main__":

#     #Start the app on port 3000, it will be different once hosted
#     app.run(port=33002, debug=True)

from flask import Flask, render_template, json
import os
import database.db_connector as db
# import database.db_credentials as db_creds

# Configuration

app = Flask(__name__)
# db_connection = db.connect_to_database(db_creds.host, db_creds.user, db_creds.passwd, db_creds.db)
db_connection = db.connect_to_database()

# Routes 

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/bsg-people')
def bsg_people():
    return "This is the bsg-people route."

@app.route('/customers')
def customers():
    # Write the query and save it to a variable
    query = "SELECT * FROM Customers"

    # The way the interface between MySQL and Flask works is by using an
    # object called a cursor. Think of it as the object that acts as the
    # person typing commands directly into the MySQL command line and
    # reading them back to you when it gets results
    cursor = db.execute_query(db_connection=db_connection, query=query)

    # The cursor.fetchall() function tells the cursor object to return all
    # the results from the previously executed
    #
    # The json.dumps() function simply converts the dictionary that was
    # returned by the fetchall() call to JSON so we can display it on the
    # page.
    results = json.dumps(cursor.fetchall())

    # Sends the results back to the web browser.
    return results

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 33002)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 