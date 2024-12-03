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

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 33002)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 