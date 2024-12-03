# from flask import Flask, render_template, json, redirect
# from flask_mysqldb import MySQL
# from flask import request
# import os

# app = Flask(__name__)


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

from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db


# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()
#comes from module, is essentially MySQL(app) from starter code

# Routes 

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/bsg-people')
def bsg_people():
    return "This is the bsg-people route."

# Customers Routes
@app.route('/customers', methods = ["POST", "GET"])
def customers():
    # Write the query and save it to a variable
    if request.method == "GET":
        query = "SELECT * FROM Customers"
        cursor = db.execute_query(db_connection=db_connection, query=query)

        # The cursor.fetchall() function tells the cursor object to return all
        # the results from the previously executed
        results = cursor.fetchall()
        
        # Sends the results back to the web browser.
        return render_template("customers.j2", customers = results)
        
        # For testing purposes to see json.
        # results = json.dumps(cursor.fetchall())
        # return results

    if request.method == "POST":
        # runs if user presses add button
        if request.form.get("Add_Customer"):
            # grabs user form inputs
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]

            # no null inputs
            query = "INSERT INTO Customers (name, email, phone) VALUES (%s, %s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name,email,phone))
            results = cursor.fetchall()

        # redirect back to customers page
        return redirect("/customers")

@app.route("/delete_customer/<int:customerID>")
def delete_customer(customerID):
    #mySQL query to delete the person with passed ID
    query = "DELETE FROM Customers WHERE customerID = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customerID,)) #keep comma, required idk why 

    return redirect("/customers")

@app.route("/edit_customer/<int:customerID>", methods=["POST", "GET"])
def edit_customer(customerID):
    if request.method == "GET":
        query = "SELECT * FROM Customers WHERE customerID = %s" % (customerID)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("customers_edit.j2", data=data)
    
    if request.method == "POST":
        # runs if user presses 'Edit Customer' button
        if request.form.get("Edit_Customer"):
            # grabs user form inputs
            id = request.form["customerID"]
            name = request.form["name"]
            email = request.form["email"]
            phone = request.form["phone"]

            # no null inputs
            query = "UPDATE Customers SET Customers.name = %s, Customers.email = %s, Customers.phone = %s WHERE Customers.customerID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(name,email,phone, id))
            results = cursor.fetchall()

        # redirect back to customers page
        return redirect("/customers")


# Orders
@app.route('/orders', methods = ["POST", "GET"])
def orders():
    # Write the query and save it to a variable
    if request.method == "GET":
        query = "SELECT * FROM Orders"
        cursor = db.execute_query(db_connection=db_connection, query=query)

        # The cursor.fetchall() function tells the cursor object to return all
        # the results from the previously executed
        results = cursor.fetchall()

        
        # Query to grab customer ID's for dropdown.
        query2 = "SELECT customerID from Customers"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        customerid_data = cursor.fetchall()

        
        # Sends the results back to the web browser.
        return render_template("orders.j2", orders = results, customers = customerid_data)
        
        # For testing purposes to see json.
        # results = json.dumps(cursor.fetchall())
        # return results

    if request.method == "POST":
        # runs if user presses add button
        if request.form.get("Add_Order"):
            # grabs user form inputs
            customer = request.form["customer"]
            orderDate = request.form["orderDate"]
            orderAmount = request.form["orderAmount"]

            # no null inputs
            query = "INSERT INTO Orders (customerID, orderDate, orderAmount) VALUES (%s, %s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customer,orderDate,orderAmount))
            results = cursor.fetchall()
            

        # redirect back to customers page
        return redirect("/orders")

@app.route("/delete_order/<int:orderID>")
def delete_order(orderID):
    #mySQL query to delete the person with passed ID
    query = "DELETE FROM Orders WHERE orderID = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(orderID,)) #keep comma, required idk why
   
    return redirect("/orders")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 33002)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 