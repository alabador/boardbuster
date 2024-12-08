from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
import database.db_connector as db


# Configuration

app = Flask(__name__, template_folder="templates")

mysql = MySQL(app)

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

        try:
            # The cursor.fetchall() function tells the cursor object to return all
            # the results from the previously executed
            results = cursor.fetchall()
            
            # Sends the results back to the web browser.
            return render_template("customers.j2", customers = results)
            
            # For testing purposes to see json.
            # results = json.dumps(cursor.fetchall())
            # return result
        except:
            print("ERROR")
        finally:
            cursor.close()


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

# Boardgames Routes
@app.route('/boardgames', methods=["POST", "GET"])
def boardgames():
    if request.method == "GET":
        try:
            # Select only the necessary columns
            query = """
            SELECT gameID, title, categoryID, playerCount, gameCost, quantity
            FROM BoardGames;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()

            # Query to grab customer ID's for dropdown.
            query2 = "SELECT categoryID from Categories"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            categories_data = cursor.fetchall()

            return render_template("boardgames.j2", boardgames=results, categories=categories_data)
        except:
            print("ERROR")
        finally:
            cursor.close()

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
        try:
            # Select necessary columns for categories
            query = """
            SELECT categoryID, categoryName, description
            FROM Categories;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()
            return render_template("categories.j2", categories=results)
        except:
            print("ERROR")
        finally:
            cursor.close()

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
        try: 
            query = """
            SELECT Orders.*, Customers.name 
            FROM Orders 
            Join Customers 
            WHERE (Orders.customerID = Customers.customerID);
            """
            cursor = db.execute_query(db_connection=db_connection, query=query)

            # The cursor.fetchall() function tells the cursor object to return all
            # the results from the previously executed
            results = cursor.fetchall()

            
            # Query to grab customer ID's for dropdown.
            query2 = "SELECT customerID, name from Customers"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            customerid_data = cursor.fetchall()

            
            # Sends the results back to the web browser.
            return render_template("orders.j2", orders = results, customers = customerid_data)
            
            # For testing purposes to see json.
            # results = json.dumps(cursor.fetchall())
            # return results
        except:
            print("ERROR")
        finally:
            cursor.close()

    if request.method == "POST":
        # runs if user presses add button
        if request.form.get("Add_Order"):
            # grabs user form inputs
            customer = request.form["customer"]
            orderDate = request.form["orderDate"]

            # no null inputs
            query = "INSERT INTO Orders (customerID, orderDate) VALUES (%s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(customer,orderDate))
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
        query = """
        SELECT Orders.*, Customers.name 
        FROM Orders 
        Join Customers 
        WHERE (Orders.customerID = Customers.customerID)
        AND (Orders.orderID = %s);
        """ % (orderID)
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
        try: 
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
        except:
            print("ERROR")
        finally:
            cursor.close()

    if request.method == "POST":
        # runs if user presses add button
        if request.form.get("Add_Order_Detail"):
            # grabs user form inputs
            order = request.form["order"]
            game = request.form["game"]
            quantity = request.form["quantity"]

            # no null inputs
            query = "INSERT INTO OrderDetails (orderID, gameID, quantity) VALUES (%s, %s, %s)"
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(order,game,quantity))

            # Updates the orders entry with total price.
            update_totalprice = """
            UPDATE Orders
            SET Orders.orderAmount = (
                SELECT SUM(BoardGames.gameCost * OrderDetails.quantity)
                FROM OrderDetails
                JOIN BoardGames ON OrderDetails.gameID = BoardGames.gameID
                WHERE OrderDetails.orderID = Orders.orderID
            )
            WHERE Orders.orderID = %s
            """ % (order)
            cursor = db.execute_query(db_connection=db_connection, query=update_totalprice)
            results = cursor.fetchall()
            

        # redirect back to customers page
        return redirect("/orderdetails")

@app.route("/delete_orderdetail/<int:orderDetailID>/<int:orderID>")
def delete_orderdetail(orderDetailID, orderID):

    #mySQL query to delete the orderDetail with passed ID
    query = "DELETE FROM OrderDetails WHERE orderDetailID = '%s';"
    cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(orderDetailID,)) #keep comma, required idk why


    update_totalprice = """
    UPDATE Orders
    SET Orders.orderAmount = (
        SELECT IFNULL(SUM(BoardGames.gameCost * OrderDetails.quantity), 0)
        FROM OrderDetails
        JOIN BoardGames ON OrderDetails.gameID = BoardGames.gameID
        WHERE OrderDetails.orderID = Orders.orderID
    )
    WHERE Orders.orderID = %s
    """ % (orderID)
    cursor = db.execute_query(db_connection=db_connection, query=update_totalprice)

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
    
@app.route('/rentals', methods=["POST", "GET"])
def rentals():
    if request.method == "GET":
        try:
            # Select necessary columns for rentals
            query = """
            SELECT Rentals.rentalID, Rentals.customerID, Rentals.rentalDate, Rentals.returnDate, Rentals.rentalCost, Customers.name AS customerName
            FROM Rentals
            LEFT JOIN Customers ON Rentals.customerID = Customers.customerID;

            """
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()

            # Query to grab customer IDs for dropdown
            query2 = "SELECT customerID, name FROM Customers;"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            customers_data = cursor.fetchall()

            return render_template("rentals.j2", rentals=results, customers=customers_data)
        except Exception as e:
            print(f"Error fetching rentals: {e}")
        finally:
            cursor.close()

    if request.method == "POST":
        if request.form.get("Add_Rental"):
            # Retrieve form data
            customerID = request.form["customerID"]
            rentalDate = request.form["rentalDate"]
            returnDate = request.form.get("returnDate") or None  # Set to None if empty
            rentalCost = request.form["rentalCost"]

            # Insert new rental
            query = """
            INSERT INTO Rentals (customerID, rentalDate, returnDate, rentalCost)
            VALUES (%s, %s, %s, %s);
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(customerID, rentalDate, returnDate, rentalCost))
        return redirect("/rentals")


@app.route("/delete_rental/<int:rentalID>")
def delete_rental(rentalID):
    # Delete the rental by its ID
    query = "DELETE FROM Rentals WHERE rentalID = %s;"
    db.execute_query(db_connection=db_connection, query=query, query_params=(rentalID,))
    return redirect("/rentals")


@app.route("/edit_rental/<int:rentalID>", methods=["POST", "GET"])
def edit_rental(rentalID):
    if request.method == "GET":
        try:
            # Fetch the specific rental for editing
            query = """
            SELECT rentalID, customerID, rentalDate, returnDate, rentalCost
            FROM Rentals
            WHERE rentalID = %s;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(rentalID,))
            data = cursor.fetchall()

            # Query to grab customer IDs for dropdown
            query2 = "SELECT customerID, name FROM Customers;"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            customers_data = cursor.fetchall()

            return render_template("rentals_edit.j2", data=data, customers=customers_data)
        except Exception as e:
            print(f"Error fetching rental for editing: {e}")
        finally:
            cursor.close()

    if request.method == "POST":
        if request.form.get("Edit_Rental"):
            # Retrieve updated form data
            rentalID = request.form["rentalID"]
            customerID = request.form["customerID"]
            rentalDate = request.form["rentalDate"]
            returnDate = request.form.get("returnDate") or None  # Set to None if empty
            rentalCost = request.form["rentalCost"]

            # Update rental details
            query = """
            UPDATE Rentals
            SET customerID = %s, rentalDate = %s, returnDate = %s, rentalCost = %s
            WHERE rentalID = %s;
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(customerID, rentalDate, returnDate, rentalCost, rentalID))
        return redirect("/rentals")
    
    
@app.route('/rentaldetails', methods=["POST", "GET"])
def rentaldetails():
    if request.method == "GET":
        try:
            # Fetch rental details
            query = """
            SELECT RentalDetails.rentalDetailID, RentalDetails.rentalID, RentalDetails.gameID, 
                   BoardGames.title AS gameTitle, RentalDetails.rentalDuration, RentalDetails.rentalPrice
            FROM RentalDetails
            JOIN BoardGames ON RentalDetails.gameID = BoardGames.gameID;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query)
            results = cursor.fetchall()

            # Fetch rentals for dropdown
            query2 = "SELECT rentalID FROM Rentals;"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            rentals_data = cursor.fetchall()

            # Fetch games for dropdown
            query3 = "SELECT gameID, title FROM BoardGames;"
            cursor = db.execute_query(db_connection=db_connection, query=query3)
            games_data = cursor.fetchall()

            return render_template("rentaldetails.j2", rentaldetails=results, rentals=rentals_data, games=games_data)
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            cursor.close()

    if request.method == "POST":
        if request.form.get("Add_RentalDetail"):
            # Retrieve form data
            rentalID = request.form["rentalID"]
            gameID = request.form["gameID"]
            rentalDuration = request.form["rentalDuration"]
            rentalPrice = request.form["rentalPrice"]

            # Insert new rental detail
            query = """
            INSERT INTO RentalDetails (rentalID, gameID, rentalDuration, rentalPrice)
            VALUES (%s, %s, %s, %s);
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(rentalID, gameID, rentalDuration, rentalPrice))
        return redirect("/rentaldetails")


@app.route("/delete_rentaldetail/<int:rentalDetailID>")
def delete_rentaldetail(rentalDetailID):
    try:
        # Delete the rental detail by its ID
        query = "DELETE FROM RentalDetails WHERE rentalDetailID = %s;"
        db.execute_query(db_connection=db_connection, query=query, query_params=(rentalDetailID,))
        return redirect("/rentaldetails")
    except Exception as e:
        print(f"ERROR: {e}")


@app.route("/edit_rentaldetail/<int:rentalDetailID>", methods=["POST", "GET"])
def edit_rentaldetail(rentalDetailID):
    if request.method == "GET":
        try:
            # Fetch specific rental detail for editing
            query = """
            SELECT RentalDetails.rentalDetailID, RentalDetails.rentalID, RentalDetails.gameID, 
                   RentalDetails.rentalDuration, RentalDetails.rentalPrice, BoardGames.title AS gameTitle
            FROM RentalDetails
            JOIN BoardGames ON RentalDetails.gameID = BoardGames.gameID
            WHERE RentalDetails.rentalDetailID = %s;
            """
            cursor = db.execute_query(db_connection=db_connection, query=query, query_params=(rentalDetailID,))
            data = cursor.fetchall()

            # Fetch rentals for dropdown
            query2 = "SELECT rentalID FROM Rentals;"
            cursor = db.execute_query(db_connection=db_connection, query=query2)
            rentals_data = cursor.fetchall()

            # Fetch games for dropdown
            query3 = "SELECT gameID, title FROM BoardGames;"
            cursor = db.execute_query(db_connection=db_connection, query=query3)
            games_data = cursor.fetchall()

            return render_template("rentaldetails_edit.j2", data=data, rentals=rentals_data, games=games_data)
        except Exception as e:
            print(f"ERROR: {e}")
        finally:
            cursor.close()

    if request.method == "POST":
        if request.form.get("Edit_RentalDetail"):
            # Retrieve updated form data
            rentalDetailID = request.form["rentalDetailID"]
            rentalID = request.form["rentalID"]
            gameID = request.form["gameID"]
            rentalDuration = request.form["rentalDuration"]
            rentalPrice = request.form["rentalPrice"]

            # Update rental detail
            query = """
            UPDATE RentalDetails
            SET rentalID = %s, gameID = %s, rentalDuration = %s, rentalPrice = %s
            WHERE rentalDetailID = %s;
            """
            db.execute_query(db_connection=db_connection, query=query, query_params=(rentalID, gameID, rentalDuration, rentalPrice, rentalDetailID))
        return redirect("/rentaldetails")


# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 57294)) 
    #                                 ^^^^
    #              You can replace this number with any valid port
    
    app.run(port=port, debug=True) 