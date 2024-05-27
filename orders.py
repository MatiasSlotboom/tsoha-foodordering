from db import db
from sqlalchemy.sql import text
import user

def addOrder(restaurantName: str, orderedFoods: list):
    try:
        sql = text("SELECT name, rating FROM Restaurants")
        result = db.session.execute(sql)
        restaurants = result.fetchall()
        return restaurants
    except:
        return []