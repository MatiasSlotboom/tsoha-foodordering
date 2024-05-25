from db import db
from sqlalchemy.sql import text
import user

def getRestaurants():
    try:
        sql = text("SELECT id, name, rating FROM Restaurants")
        result = db.session.execute(sql)
        restaurants = result.fetchall()
        return restaurants
    except:
        return []

def getRestaurantsWithFood():
    try:
        parsedRestaurantData = []
        restaurantNamesAndIds = getRestaurants()
        #print(restaurantNamesAndIds)
        for restaurant in restaurantNamesAndIds:
            sql = text("SELECT f.name AS foodName, f.description AS foodDescription, f.price AS foodPrice FROM Restaurants r JOIN Foods f ON r.id = f.restaurantId WHERE r.id=:restaurantId")
            result = db.session.execute(sql, {"restaurantId":restaurant.id})
            foods = result.fetchall()
            if len(foods) == 0:
                continue
            #print("PYTHON IS BAD")
            #print("Foods", foods)
            parsedRestaurantData.append([restaurant.name, foods])
            #print("I AM AN ACTUAL COMPETENT REAL LANGUAGE AND CAN PERFORM BASIC APPENDATION")
        return parsedRestaurantData
    except Exception as ex:
        print(ex)
        return []

def getRestaurantsOwnedByUser(userId):
    try:
        sql = text("SELECT r.id, r.name FROM Restaurants r JOIN UserRestaurants ur ON r.id=ur.restaurantId WHERE ur.userId=:userId")
        result = db.session.execute(sql, {"userId":userId})
        restaurants = result.fetchall()
        return restaurants
    except:
        return []

def apply_restaurant(restaurantName, username):
    try:
        sql = text("INSERT INTO RestaurantApplications (name, applier, applierId) VALUES (:name, :applier, :applierId)")
        db.session.execute(sql, {"name":restaurantName, "applier":username, "applierId":user.getIdForUsername(username)})
        db.session.commit()
        return True
    except:
        return False
    
def getRestaurantApplications():
    try:
        sql = text("SELECT name, applier FROM RestaurantApplications")
        result = db.session.execute(sql)
        restaurants = result.fetchall()
        return restaurants
    except:
        return []

def acceptRestaurantApplication(restaurantName):
    try:
        sql = text("SELECT applierId FROM RestaurantApplications where name=:restaurantname")
        result = db.session.execute(sql, {"restaurantname":restaurantName})
        restaurantappl = result.fetchone()

        sql = text("DELETE FROM RestaurantApplications WHERE name=:restaurantname")
        db.session.execute(sql, {"restaurantname":restaurantName})
        db.session.commit()
        sql = text("INSERT INTO Restaurants (name) VALUES(:restaurantname) RETURNING id")
        result = db.session.execute(sql, {"restaurantname":restaurantName})
        db.session.commit()
        restaurant = result.fetchone()
        sql = text("INSERT INTO UserRestaurants (userId, restaurantId) VALUES(:applierId, :restaurantId)")
        db.session.execute(sql, {"applierId":restaurantappl[0], "restaurantId":restaurant[0]})
        db.session.commit()
        return True
    except:
        return False
    
def addFoodToRestaurant(foodName, foodDescription, foodPrice, restaurantId):
    try:
        sql = text("INSERT INTO Foods (name, description, price, foodCategoryId, restaurantId) VALUES(:name, :description, :price, :foodCategoryId, :restaurantId)")
        db.session.execute(sql, {"name":foodName, "description":foodDescription, "price":foodPrice, "foodCategoryId":1, "restaurantId":restaurantId})
        db.session.commit()
        return True
    except:
        pass
    return False