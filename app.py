from flask import Flask
from dotenv import load_dotenv
from os import getenv
from flask_wtf import CSRFProtect

load_dotenv()
app = Flask(__name__)
app.secret_key = getenv("SECRET_KEY")
csrf = CSRFProtect(app)

csrf.init_app(app)
import routes