-- Customers CRUD Operations

-- Select (View All Customers)
SELECT * FROM Customers;

-- Insert (Add New Customer)
INSERT INTO Customers (name, email, phone) VALUES (?, ?, ?);

-- Update (Modify Existing Customer)
UPDATE Customers SET name = ?, email = ?, phone = ? WHERE customerID = ?;

-- Delete (Remove Customer)
DELETE FROM Customers WHERE customerID = ?;

-- BoardGames CRUD Operations

-- Select (View All Board Games)
SELECT * FROM BoardGames;

-- Insert (Add New Board Game)
INSERT INTO BoardGames (title, categoryID, playerCount, gameCost, isAvailable, quantity) VALUES (?, ?, ?, ?, ?, ?);

-- Update (Modify Existing Board Game)
UPDATE BoardGames SET title = ?, categoryID = ?, playerCount = ?, gameCost = ?, isAvailable = ?, quantity = ? WHERE gameID = ?;

-- Delete (Remove Board Game)
DELETE FROM BoardGames WHERE gameID = ?;

-- Orders CRUD Operations

-- Select (View All Orders)
SELECT * FROM Orders;

-- Insert (Add New Order)
INSERT INTO Orders (customerID, orderDate, orderAmount) VALUES (?, ?, ?);

-- Update (Modify Existing Order)
UPDATE Orders SET customerID = ?, orderDate = ?, orderAmount = ? WHERE orderID = ?;

-- Delete (Remove Order)
DELETE FROM Orders WHERE orderID = ?;

-- Rentals CRUD Operations

-- Select (View All Rentals)
SELECT * FROM Rentals;

-- Insert (Add New Rental)
INSERT INTO Rentals (customerID, rentalDate, returnDate, rentalCost) VALUES (?, ?, ?, ?);

-- Update (Modify Existing Rental)
UPDATE Rentals SET customerID = ?, rentalDate = ?, returnDate = ?, rentalCost = ? WHERE rentalID = ?;

-- Delete (Remove Rental)
DELETE FROM Rentals WHERE rentalID = ?;
