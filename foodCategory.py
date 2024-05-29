from db import db
from sqlalchemy.sql import text
from app import app

def initialiseFoodCategories():
    #Check if table is empty
    with app.app_context():
        sql = text("SELECT EXISTS (SELECT 0 FROM FoodCategories)")
        result = db.session.execute(sql)
        isEmpty = result.fetchone()[0]
        if isEmpty == False:
            sql = text("INSERT INTO FoodCategories (name) VALUES('error')")
            db.session.execute(sql)
            db.session.commit()