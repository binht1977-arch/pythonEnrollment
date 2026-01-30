#from flask_mongoengine2 import MongoEngine # type: ignore
from flask_restx import Api # type: ignore

from flask import Flask
#from flask import render_template
from config import Config
from flask_mongoengine2 import MongoEngine  
#from flask_restplus import Api


app = Flask(__name__)
app.config.from_object(Config)

db = MongoEngine()
db.init_app(app)


api = Api(
    version='1.0',
    title='Enrollment API',
    description='A comprehensive Enrollment Management API',
    #doc='/docs',  # Optional: Custom Swagger documentation path
    default='Enrollment',  # This changes the default namespace
    default_label='Enrollment operations'
)
api.init_app(app)

# Import routes to register them with the app
from application import routes
