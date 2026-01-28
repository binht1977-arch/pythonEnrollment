#from flask_mongoengine2 import MongoEngine # type: ignore
#from flask_restx import Api # type: ignore

from flask import Flask
#from flask import render_template
from config import Config
from flask_mongoengine2 import MongoEngine  


app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)

# Import routes to register them with the app
from application import routes
