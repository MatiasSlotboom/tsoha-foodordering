from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv, getuid
import pwd

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL").replace("currentusernamedonotchange", pwd.getpwuid(getuid()).pw_name)
db = SQLAlchemy(app)