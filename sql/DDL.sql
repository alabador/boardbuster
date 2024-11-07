-- Disable foreign key checks
SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Drop tables if they already exist
DROP TABLE IF EXISTS BoardGames, Customers, Rentals, RentalDetails, Orders, OrderDetails, Categories;

-- BoardGames Table
CREATE TABLE BoardGames (
    gameID INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    categoryID INT,  -- Foreign key to Categories
    playerCount TINYINT NOT NULL,
    gameCost DECIMAL(6,2) NOT NULL,
    isAvailable BOOL NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (categoryID) REFERENCES Categories(categoryID) ON DELETE SET NULL
);

-- Customers Table
CREATE TABLE Customers (
    customerID INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(15) NOT NULL
);

-- Rentals Table
CREATE TABLE Rentals (
    rentalID INT PRIMARY KEY AUTO_INCREMENT,
    customerID INT NOT NULL,  -- Foreign key to Customers
    rentalDate DATE NOT NULL,
    returnDate DATE,
    rentalCost DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE
);

-- RentalDetails Table
CREATE TABLE RentalDetails (
    rentalDetailID INT PRIMARY KEY AUTO_INCREMENT,
    rentalID INT NOT NULL,  -- Foreign key to Rentals
    gameID INT NOT NULL,    -- Foreign key to BoardGames
    rentalDuration INT NOT NULL,  -- e.g., hours rented
    rentalPrice DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (rentalID) REFERENCES Rentals(rentalID) ON DELETE CASCADE,
    FOREIGN KEY (gameID) REFERENCES BoardGames(gameID) ON DELETE CASCADE
);

-- Orders Table
CREATE TABLE Orders (
    orderID INT PRIMARY KEY AUTO_INCREMENT,
    customerID INT NOT NULL,  -- Foreign key to Customers
    orderDate DATE NOT NULL,
    orderAmount DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID) ON DELETE CASCADE
);

-- OrderDetails Table
CREATE TABLE OrderDetails (
    orderDetailID INT PRIMARY KEY AUTO_INCREMENT,
    orderID INT NOT NULL,  -- Foreign key to Orders
    gameID INT NOT NULL,    -- Foreign key to BoardGames
    quantity INT NOT NULL,
    price DECIMAL(8,2) NOT NULL,
    FOREIGN KEY (orderID) REFERENCES Orders(orderID) ON DELETE CASCADE,
    FOREIGN KEY (gameID) REFERENCES BoardGames(gameID) ON DELETE CASCADE
);

-- Categories Table
CREATE TABLE Categories (
    categoryID INT PRIMARY KEY AUTO_INCREMENT,
    categoryName VARCHAR(100) NOT NULL,
    description VARCHAR(255)
);

/* 

    INSERTING EXAMPLE DATA
    
*/
-- Categories Table
INSERT INTO Categories (categoryName, description) VALUES 
('Party Games', 'Games ideal for parties and large groups'),
('Strategy', 'Games requiring strategy and planning'),
('Family', 'Games suitable for all ages'),
('Card Games', 'Games played with cards');

-- BoardGames Table
INSERT INTO BoardGames (title, categoryID, playerCount, gameCost, isAvailable, quantity) VALUES 
('Monopoly', 2, 4, 29.99, TRUE, 10),
('Catan', 2, 4, 39.99, TRUE, 5),
('Uno', 4, 2, 9.99, TRUE, 20),
('Pandemic', 2, 4, 34.99, FALSE, 0),
('Exploding Kittens', 1, 5, 19.99, TRUE, 15);

-- Customers Table
INSERT INTO Customers (name, email, phone) VALUES 
('John Doe', 'johndoe@example.com', '5551234567'),
('Jane Smith', 'janesmith@example.com', '5559876543'),
('Austin Texas', 'austintexas@example.com', '5554441234'),
('Billy Jean', 'billyjean@example.com', '5554206969');

-- Rentals Table
INSERT INTO Rentals (customerID, rentalDate, returnDate, rentalCost) VALUES 
(1, '2024-01-10', '2024-01-11', 5.99),
(2, '2024-01-11', '2024-01-12', 8.99),
(3, '2024-01-12', NULL, 10.99);

-- RentalDetails Table
INSERT INTO RentalDetails (rentalID, gameID, rentalDuration, rentalPrice) VALUES 
(1, 1, 24, 5.99),
(1, 3, 24, 3.99),
(2, 2, 48, 8.99),
(3, 4, 72, 10.99);

-- Orders Table
INSERT INTO Orders (customerID, orderDate, orderAmount) VALUES 
(1, '2024-02-01', 59.98),
(2, '2024-02-02', 19.99),
(3, '2024-02-03', 29.99),
(4, '2024-02-04', 39.99);

-- OrderDetails Table
INSERT INTO OrderDetails (orderID, gameID, quantity, price) VALUES 
(1, 1, 2, 29.99),
(1, 2, 1, 39.99),
(2, 5, 1, 19.99),
(3, 4, 1, 29.99),
(4, 2, 1, 39.99);

-- Query and retrieve data from tables

SELECT * FROM BoardGames;
SELECT * FROM Customers;
SELECT * FROM Rentals;
SELECT * FROM RentalDetails;
SELECT * FROM Orders;
SELECT * FROM OrderDetails;
SELECT * FROM Categories;

-- Enable foreign key checks
SET FOREIGN_KEY_CHECKS=1;
COMMIT;