from db import db
from sqlalchemy.sql import text

def getFoodId(foodName):
    try:
        sql = text("SELECT f.id FROM Foods f WHERE f.description=:foodName")
        result = db.session.execute(sql, {"foodName":foodName})
        foodId = result.fetchone()[0]
        if foodId == None:
            return 0
        return foodId
    except:
        return 0