-- Customers CRUD Operations

-- Select (View All Customers)
SELECT * FROM Customers;

-- Insert (Add New Customer)
INSERT INTO Customers (name, email, phone) 
VALUES (?, ?, ?);

-- Update (Modify Existing Customer)
UPDATE Customers 
SET name = ?, email = ?, phone = ? 
WHERE customerID = ?;

-- Delete (Remove Customer)
DELETE FROM Customers 
WHERE customerID = ?;


-- BoardGames CRUD Operations

-- Select (View All Board Games with Categories)
SELECT BoardGames.gameID, BoardGames.title, Categories.categoryName, 
       BoardGames.playerCount, BoardGames.gameCost, BoardGames.quantity
FROM BoardGames
JOIN Categories ON BoardGames.categoryID = Categories.categoryID;

-- Insert (Add New Board Game)
INSERT INTO BoardGames (title, categoryID, playerCount, gameCost, quantity) 
VALUES (?, ?, ?, ?, ?);

-- Update (Modify Existing Board Game)
UPDATE BoardGames 
SET title = ?, categoryID = ?, playerCount = ?, gameCost = ?, quantity = ? 
WHERE gameID = ?;

-- Delete (Remove Board Game)
DELETE FROM BoardGames 
WHERE gameID = ?;


-- Categories CRUD Operations

-- Select (View All Categories)
SELECT categoryID, categoryName, description 
FROM Categories;

-- Insert (Add New Category)
INSERT INTO Categories (categoryName, description) 
VALUES (?, ?);

-- Update (Modify Existing Category)
UPDATE Categories 
SET categoryName = ?, description = ? 
WHERE categoryID = ?;

-- Delete (Remove Category)
DELETE FROM Categories 
WHERE categoryID = ?;


-- Orders CRUD Operations

-- Select (View All Orders with Customer Names)
SELECT Orders.orderID, Orders.customerID, Orders.orderDate, Orders.orderAmount, Customers.name
FROM Orders
JOIN Customers ON Orders.customerID = Customers.customerID;

-- Insert (Add New Order)
INSERT INTO Orders (customerID, orderDate) 
VALUES (?, ?);

-- Update (Modify Existing Order)
UPDATE Orders 
SET orderDate = ? 
WHERE orderID = ?;

-- Delete (Remove Order)
DELETE FROM Orders 
WHERE orderID = ?;


-- OrderDetails CRUD Operations

-- Select (View All Order Details with Games and Customer Names)
SELECT OrderDetails.orderDetailID, OrderDetails.orderID, OrderDetails.gameID, 
       OrderDetails.quantity, BoardGames.title, Customers.name
FROM OrderDetails
JOIN BoardGames ON OrderDetails.gameID = BoardGames.gameID
JOIN Orders ON OrderDetails.orderID = Orders.orderID
JOIN Customers ON Orders.customerID = Customers.customerID;

-- Insert (Add New Order Detail)
INSERT INTO OrderDetails (orderID, gameID, quantity) 
VALUES (?, ?, ?);

-- Update (Modify Existing Order Detail)
UPDATE OrderDetails 
SET orderID = ?, gameID = ?, quantity = ? 
WHERE orderDetailID = ?;

-- Delete (Remove Order Detail)
DELETE FROM OrderDetails 
WHERE orderDetailID = ?;


-- Rentals CRUD Operations

-- Select (View All Rentals with Customer Names)
SELECT Rentals.rentalID, Rentals.customerID, Rentals.rentalDate, Rentals.returnDate, Rentals.rentalCost, Customers.name
FROM Rentals
JOIN Customers ON Rentals.customerID = Customers.customerID;

-- Insert (Add New Rental)
INSERT INTO Rentals (customerID, rentalDate, returnDate, rentalCost) 
VALUES (?, ?, ?, ?);

-- Update (Modify Existing Rental)
UPDATE Rentals 
SET customerID = ?, rentalDate = ?, returnDate = ?, rentalCost = ? 
WHERE rentalID = ?;

-- Delete (Remove Rental)
DELETE FROM Rentals 
WHERE rentalID = ?;


-- RentalDetails CRUD Operations

-- Select (View All Rental Details with Game Titles)
SELECT RentalDetails.rentalDetailID, RentalDetails.rentalID, RentalDetails.gameID, 
       RentalDetails.rentalDuration, RentalDetails.rentalPrice, BoardGames.title
FROM RentalDetails
JOIN BoardGames ON RentalDetails.gameID = BoardGames.gameID;

-- Insert (Add New Rental Detail)
INSERT INTO RentalDetails (rentalID, gameID, rentalDuration, rentalPrice) 
VALUES (?, ?, ?, ?);

-- Update (Modify Existing Rental Detail)
UPDATE RentalDetails 
SET rentalID = ?, gameID = ?, rentalDuration = ?, rentalPrice = ? 
WHERE rentalDetailID = ?;

-- Delete (Remove Rental Detail)
DELETE FROM RentalDetails 
WHERE rentalDetailID = ?;
