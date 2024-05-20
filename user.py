from werkzeug.security import check_password_hash, generate_password_hash
from flask import session
from db import db
from sqlalchemy.sql import text
from os import getenv

def getIdForUsername(username):
    sql = text("SELECT id FROM Users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return -1
    else:
        return user.id

def login(username, password):
    sql = text("SELECT id, password, isadmin FROM Users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()

    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["displayname"] = username
            session["isAdmin"] = user.isadmin
            
            try:
                sql = text("SELECT restaurantId FROM UserRestaurants WHERE userId=:userId")
                result = db.session.execute(sql, {"userId":user.id})
                restaurant = result.fetchone()
                if restaurant:
                    session["hasRestaurant"] = True
                else:
                    session["hasRestaurant"] = False
            except:
                session["hasRestaurant"] = False
            return True
        else:
            return False
        
def register(username, password):
    #Check whether user exists already first
    sql = text("SELECT id FROM Users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if user:
        return False
    else:
        try:
            sql = text("INSERT INTO Users (username, password, isadmin, creationDate) VALUES (:username, :password, FALSE, NOW()) RETURNING ID")
            result = db.session.execute(sql, {"username":username, "password":generate_password_hash(password)})
            user = result.fetchone()
            db.session.commit()
        except:
            return False
        
        if user:
            session["user_id"] = user.id
            session["displayname"] = username
            session["isAdmin"] = False
            return True
        else:
            return False
        
def tryDeleteValue(value: str):
    try:
        del session[value]
    except:
        pass

def logout():
    tryDeleteValue("user_id")
    tryDeleteValue("displayname")
    tryDeleteValue("isAdmin")
    tryDeleteValue("hasRestaurant")

def user_id():
    return session.get("user_id",0)

def has_restaurant():
    return session.get("hasRestaurant",0)
    
def user_displayname():
    return session.get("displayname",0)

def user_name():
    sql = text("SELECT username FROM Users WHERE id=:id")
    result = db.session.execute(sql, {"id":user_id()})
    user = result.fetchone()

    if not user:
        return "Null"
    else:
        return user.username
    
def user_isAdmin():
    sql = text("SELECT isadmin FROM Users WHERE id=:id")
    result = db.session.execute(sql, {"id":user_id()})
    user = result.fetchone()

    if user and user.isadmin == True:
        return True
    
    return False

def user_ownsRestaurant(restaurantId):
    sql = text("SELECT restaurantId FROM UserRestaurants WHERE restaurantId=:restaurantId and userId=:userId")
    result = db.session.execute(sql, {"restaurantId":restaurantId, "userId":user_id()})
    user = result.fetchone()

    if user:
        return True
    return False

def elevate_user(password):
    if password == getenv("ADMIN_PASSWORD"):
        sql = text("UPDATE Users SET isadmin=TRUE WHERE id=:id")
        result = db.session.execute(sql, {"id":user_id()})
        db.session.commit()

        if result:
            session["isAdmin"] = True
            return True
        else:
            session["isAdmin"] = False
        
    return False