from application import app 
from flask import render_template

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html',login=False)

@app.route('/course_offerings')
def course_offerings():
    return render_template('course_offerings.html')             

@app.route('/register')
def register():           
    return render_template('register.html')     

@app.route('/login')
def login():           
    return render_template('login.html')            

@app.route('/logout')
def logout():           
    return render_template('logout.html')           



