from application import app 
from flask import render_template
from flask import request, json, Response, redirect, flash
from application import db
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html',index=True)

@app.route('/login', methods=['get', 'post'])
def login():           
    form = LoginForm()
    if form.validate_on_submit():
        if request.form.get("email") == "le_duc_quan@hotmail.com":
            flash("You have successfully logged in!", "success")
            # flash("You have successfully logged in2!")
            return redirect('/index')
        else:   
            flash("Something went wrong. Please try again.", "danger")
    return render_template('login.html', title="Login", form=form, login=True)            


@app.route('/courses/')
@app.route("/courses/<term>")
def courses(term="Spring 2019"):  #example test http://127.0.0.1:5000/courses/Fall%202020
    return render_template('courses.html', courseData=courseData, courses=True, term=term)


@app.route('/register')
def register():           
    return render_template('register.html', register=True)     

@app.route('/enrollment', methods=['get', 'post'])
def enrollment():      
    id = request.form.get('courseID')
    title = request.form['title'] # same as get method above
    term = request.form.get('term')

    return render_template('enrollment.html', enrollment=True, data={'courseID': id, 'title': title, 'term': term})          

@app.route('/api/')       #http://127.0.0.1:5000/api          -- test example
@app.route('/api/<idx>')  #http://127.0.0.1:5000/api/0        -- test example
def api(idx=None):           
    if idx is None:
        jdata = courseData
    else:
        jdata = courseData[int(idx)]

    return Response(json.dumps(jdata), mimetype="application/json")


@app.route('/logout')
def logout():           
    return render_template('logout.html')           


@app.route('/user') 
def user():

     users = User.objects().all()
     return render_template('user.html', users=users)    

@app.route('/add_test_users')
def add_test_users():
# insert sample user data into the database
#     user = User(user_id=100, first_name="John", last_name="Doe", email="johndoe@example.com", password="password123") \
#     .save()
#     user = User(user_id=2, first_name="Jane", last_name="Smith", email="janesmith@example.com", password="password456")\
#     .save()
     
# upsert example - update if exists, insert if not
     user = User.objects(user_id=100).update_one(
        set__first_name="John",
        set__last_name="Doe",
        set__email="johndoe@example.com",
        set__password="password125",
        upsert=True
    )

     users = User.objects(user_id = 100)
     return render_template('user.html', users=users)    




