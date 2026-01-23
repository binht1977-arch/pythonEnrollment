from flask import Flask
from flask import render_template

app = Flask(__name__)

# Import routes to register them with the app
from application import routes
