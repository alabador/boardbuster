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

@app.route('/boardgames', methods=["POST", "GET"])
def boardgames():
    if request.method == "GET":
        # Select only the necessary columns
        query = """
        SELECT gameID, title, categoryID, playerCount, gameCost, quantity
        FROM BoardGames;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("boardgames.j2", boardgames=results)

    if request.method == "POST":
        if request.form.get("Add_BoardGame"):
            # Retrieve form data
            title = request.form["title"]
            categoryID = request.form["categoryID"]
            playerCount = request.form["playerCount"]
            gameCost = request.form["gameCost"]
            quantity = request.form["quantity"]

            # Insert new board game
            query = """
            INSERT INTO BoardGames (title, categoryID, playerCount, gameCost, quantity)
            VALUES (%s, %s, %s, %s, %s);
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(title, categoryID, playerCount, gameCost, quantity))
        return redirect("/boardgames")


@app.route("/delete_boardgame/<int:gameID>")
def delete_boardgame(gameID):
    # Delete the board game by its ID
    query = "DELETE FROM BoardGames WHERE gameID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(gameID,))
    return redirect("/boardgames")


@app.route("/edit_boardgame/<int:gameID>", methods=["POST", "GET"])
def edit_boardgame(gameID):
    if request.method == "GET":
        # Fetch the specific board game for editing
        query = """
        SELECT gameID, title, categoryID, playerCount, gameCost, quantity
        FROM BoardGames
        WHERE gameID = %s;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(gameID,))
        data = cursor.fetchall()
        return render_template("boardgames_edit.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_BoardGame"):
            # Retrieve updated form data
            title = request.form["title"]
            categoryID = request.form["categoryID"]
            playerCount = request.form["playerCount"]
            gameCost = request.form["gameCost"]
            quantity = request.form["quantity"]

            # Update board game details
            query = """
            UPDATE BoardGames
            SET title = %s, categoryID = %s, playerCount = %s, gameCost = %s, quantity = %s
            WHERE gameID = %s;
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(title, categoryID, playerCount, gameCost, quantity, gameID))
        return redirect("/boardgames")
    
@app.route('/categories', methods=["POST", "GET"])
def categories():
    if request.method == "GET":
        # Select necessary columns for categories
        query = """
        SELECT categoryID, categoryName, description
        FROM Categories;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query)
        results = cursor.fetchall()
        return render_template("categories.j2", categories=results)

    if request.method == "POST":
        if request.form.get("Add_Category"):
            # Retrieve form data
            categoryName = request.form["categoryName"]
            description = request.form["description"]

            # Insert new category
            query = """
            INSERT INTO Categories (categoryName, description)
            VALUES (%s, %s);
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(categoryName, description))
        return redirect("/categories")


@app.route("/delete_category/<int:categoryID>")
def delete_category(categoryID):
    # Delete the category by its ID
    query = "DELETE FROM Categories WHERE categoryID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(categoryID,))
    return redirect("/categories")


@app.route("/edit_category/<int:categoryID>", methods=["POST", "GET"])
def edit_category(categoryID):
    if request.method == "GET":
        # Fetch the specific category for editing
        query = """
        SELECT categoryID, categoryName, description
        FROM Categories
        WHERE categoryID = %s;
        """
        cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(categoryID,))
        data = cursor.fetchall()
        return render_template("categories_edit.j2", data=data)

    if request.method == "POST":
        if request.form.get("Edit_Category"):
            # Retrieve updated form data
            categoryName = request.form["categoryName"]
            description = request.form["description"]

            # Update category details
            query = """
            UPDATE Categories
            SET categoryName = %s, description = %s
            WHERE categoryID = %s;
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(categoryName, description, categoryID))
        return redirect("/categories")

# Orders
@app.route("/orders", methods=["POST", "GET"])
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

@app.route("/edit_order/<int:orderID>", methods=["POST", "GET"])
def edit_order(orderID):
    if request.method == "GET":
        query = "SELECT * FROM Orders WHERE orderID = %s" % (orderID)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("orders_edit.j2", data=data)
    
    if request.method == "POST":
        # runs if user presses 'Edit Customer' button
        if request.form.get("Edit_Order"):
            # grabs user form inputs
            orderID = request.form["orderID"]
            customerID = request.form["customerID"]
            orderDate = request.form["orderDate"]
            orderAmount = request.form["orderAmount"]

            # no null inputs
            query = "UPDATE Orders SET Orders.customerID = %s, Orders.orderDate = %s, Orders.orderAmount = %s WHERE Orders.orderID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customerID, orderDate, orderAmount, orderID))
            results = cursor.fetchall()
        return redirect("/orders")

# OrderDetails
@app.route('/orderdetails', methods = ["POST", "GET"])
def orderdetails():
    # Write the query and save it to a variable
    if request.method == "GET":
        query = "SELECT * FROM OrderDetails"
        cursor = db.execute_query(db_connection=db_connection, query=query)

        # The cursor.fetchall() function tells the cursor object to return all
        # the results from the previously executed
        results = cursor.fetchall()
        
        # Query to grab order ID for dropdown.
        query2 = "SELECT orderID from Orders"
        cursor = db.execute_query(db_connection=db_connection, query=query2)
        order_data = cursor.fetchall()
        
        # Query to grab game ID for dropdown.
        query3 = "SELECT gameID from BoardGames"
        cursor = db.execute_query(db_connection=db_connection, query=query3)
        game_data = cursor.fetchall()

        # Sends the results back to the web browser.
        return render_template("orderdetails.j2", orderdetails = results, orders = order_data, games = game_data)
        
        # For testing purposes to see json.
        # results = json.dumps(cursor.fetchall())
        # return results

    if request.method == "POST":
        # runs if user presses add button
        if request.form.get("Add_Order_Detail"):
            # grabs user form inputs
            order = request.form["order"]
            game = request.form["game"]
            price = request.form["price"]
            quantity = request.form["quantity"]

            # no null inputs
            query = "INSERT INTO OrderDetails (orderID, gameID, quantity, price) VALUES (%s, %s, %s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(order,game,quantity,price))
            results = cursor.fetchall()
            

        # redirect back to customers page
        return redirect("/orderdetails")

@app.route("/delete_orderdetail/<int:orderDetailID>")
def delete_orderdetail(orderDetailID):
    #mySQL query to delete the orderDetail with passed ID
    query = "DELETE FROM OrderDetails WHERE orderDetailID = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(orderDetailID,)) #keep comma, required idk why
   
    return redirect("/orderdetails")

@app.route("/edit_orderdetail/<int:orderDetailID>", methods=["POST", "GET"])
def edit_orderdetail(orderDetailID):
    if request.method == "GET":
        query = "SELECT * FROM OrderDetails WHERE orderDetailID = %s" % (orderDetailID)
        cursor = db.execute_query(db_connection=db_connection, query=query)
        data = cursor.fetchall()

        return render_template("orderdetails_edit.j2", data=data)
    
    if request.method == "POST":
        # runs if user presses 'Edit Customer' button
        if request.form.get("Edit_OrderDetail"):
            # grabs user form inputs
            orderDetailID = request.form["orderDetailID"]
            orderID = request.form["orderID"]
            gameID = request.form["gameID"]
            price = request.form["price"]
            quantity = request.form["quantity"]

            # no null inputs
            query = "UPDATE OrderDetails SET OrderDetails.orderID = %s, OrderDetails.gameID = %s, OrderDetails.quantity = %s, OrderDetails.price = %s WHERE OrderDetails.orderDetailID = %s;"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(orderID, gameID, quantity, price, orderDetailID))
            results = cursor.fetchall()
        return redirect("/orderdetails")

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 33002)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 