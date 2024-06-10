CREATE TABLE Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(32) UNIQUE NOT NULL,
    password VARCHAR(162) NOT NULL, /*Make this the length of the hash*/
    isadmin BOOLEAN NOT NULL,
    creationDate TIMESTAMP NOT NULL
);

CREATE TABLE Restaurants (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL,
    rating DECIMAL(2, 1)
);

CREATE TABLE RestaurantApplications (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL,
    applier VARCHAR(32) NOT NULL,
    applierId INT REFERENCES Users(id)
);

CREATE TABLE FoodCategories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) UNIQUE NOT NULL
);

CREATE TABLE Foods (
    id SERIAL PRIMARY KEY,
    name VARCHAR(32) NOT NULL,
    description VARCHAR(128),
    price DECIMAL(5, 2) NOT NULL,
    foodCategoryId INT REFERENCES FoodCategories(id),
    restaurantId INT REFERENCES Restaurants(id)
);

CREATE TABLE Orders (
    id SERIAL PRIMARY KEY,
    userId INT REFERENCES Users(id),
    restaurantId INT REFERENCES Restaurants(id),
    orderDate TIMESTAMP NOT NULL
);

CREATE TABLE OrderInformation (
    orderId INT REFERENCES Orders(id),
    foodId INT REFERENCES Foods(id),
    amount INT NOT NULL,
    PRIMARY KEY(orderId, foodId)
);

CREATE TABLE Menus (
    id SERIAL PRIMARY KEY,
    foodId INT REFERENCES Foods(id),
    restaurantId INT REFERENCES Restaurants(id)
);

CREATE TABLE UserRestaurants (
    userId INT REFERENCES Users(id),
    restaurantId INT REFERENCES Restaurants(id),
    PRIMARY KEY(userId, restaurantId)
);