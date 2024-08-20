from db import db
from sqlalchemy.sql import text
from datetime import datetime
import user, restaurants, food

def processRequestFormToOrderedFoods(requestForm: list):
    orderedFoods = []
    restaurantName = ""
    for key in requestForm:
        if key == "csrf_token":
            continue
        value = requestForm[key]
        if key == "restaurantName":
            restaurantName = value
            continue

        if value != "" and int(value) > 0:
            orderedFoods.append((key, int(value)))
    return restaurantName, orderedFoods
        

def addOrder(requestForm: list, userId):

    restaurantName, orderedFoods = processRequestFormToOrderedFoods(requestForm)
    restaurantId = restaurants.getRestaurantId(restaurantName)
    print(restaurantName)
    print(orderedFoods)
    print(restaurantId)
    
    try:
        sql = text("INSERT INTO Orders (userId, restaurantId, orderDate) VALUES (:userId, :restaurantId, NOW()) RETURNING ID")
        result = db.session.execute(sql, {"userId":userId, "restaurantId":restaurantId})
        orderId = result.fetchone()[0]
        print(orderedFoods)

        for foodName, amount in orderedFoods:
            foodId = food.getFoodId(foodName)
            if foodId == 0:
                print("Food with name", foodName, "not found!")
                continue
            sql = text("INSERT INTO OrderInformation (orderId, foodId, amount) VALUES (:orderId, :foodId, :foodamount)")
            print(foodId, amount)
            result = db.session.execute(sql, {"orderId":orderId, "foodId":foodId , "foodamount":amount})

        db.session.commit()
        return True
    except:
        return False
    

def getAllOrdersByUser(userId):
    try:
        sql = text("SELECT Foods.name, OrderInformation.amount, Orders.orderDate, Restaurants.name FROM Orders JOIN OrderInformation ON Orders.id = OrderInformation.orderId JOIN Foods ON OrderInformation.foodId = Foods.id JOIN Restaurants ON Orders.restaurantId = Restaurants.id WHERE Orders.userId = :userId ORDER BY Orders.orderDate DESC;")
        result = db.session.execute(sql, {"userId":userId})
        orders = result.fetchall()
        return orders
    except Exception as ex:
        print(ex)
        return []

def getAllOrdersToUser(userId):
    try:
        if user.user_isAdmin():
            sql = text("SELECT Foods.name, OrderInformation.amount, Orders.orderDate, Restaurants.name, Users.username FROM Orders JOIN OrderInformation ON Orders.id = OrderInformation.orderId JOIN Foods ON OrderInformation.foodId = Foods.id JOIN Users ON Orders.userId = Users.id JOIN Restaurants ON Orders.restaurantId = Restaurants.id JOIN Users AdminUser ON AdminUser.id = :userId WHERE AdminUser.isAdmin = TRUE ORDER BY Orders.orderDate DESC;")
        else:
            sql = text("SELECT Foods.name, OrderInformation.amount, Orders.orderDate, Restaurants.name, Users.username FROM Orders JOIN OrderInformation ON Orders.id = OrderInformation.orderId JOIN Foods ON OrderInformation.foodId = Foods.id JOIN Users ON Orders.userId = Users.id JOIN Restaurants ON Orders.restaurantId = Restaurants.id WHERE Restaurants.ownerId = :userId ORDER BY Orders.orderDate DESC;")
        result = db.session.execute(sql, {"userId":userId})
        return result.fetchall()
    except Exception as ex:
        print(ex)
        return [("Error", 1, datetime(1, 1, 1, 1, 1), "You do not seem to have a restaurant", "Error")]