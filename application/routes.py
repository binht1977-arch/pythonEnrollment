from application import app 
from flask import render_template, url_for
from flask import request, json, Response, redirect, flash, session
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
    print("-LEQUAN DEBUG- Login route accessed::", session.get('username'))
    if session.get('username'):
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.objects(email=email).first()
        if user and user.get_password(password): # get_password method to check hashed password, will fail if password wasn't hashed originally
            flash(f"{user.first_name}, you have successfully logged in!", "success")
            session['user_id'] = user.user_id  # store user_id in session
            session['username'] = user.first_name


            return redirect('/index')
        else:   
            flash("Something went wrong. Please try again.", "danger")
    return render_template('login.html', title="Login", form=form, login=True)            


@app.route('/courses/')
@app.route("/courses/<term>")
def courses(term= None):  #example test http://127.0.0.1:5000/courses/Fall%202020
    if term is None:
        term = "Spring 2019"
    
    classes = Course.objects().order_by('+courseID')  # + for ascending, - for descending

    print(classes)
    return render_template('courses.html', courseData=classes, courses=True, term=term)


@app.route('/register', methods=['get', 'post'])
def register():
    if session.get('username'):
        return redirect(url_for('index'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        user_id = User.objects.count() + 1  # simple way to generate user_id

        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        print(password)
        user.set_password(password)  # hash the password before saving
        print(password)
        user.save()

        flash(f"{user.first_name}, you have successfully registered!", "success")
        return redirect(url_for('index'))
    return render_template('register.html', title="Register", form=form, register=True)     


@app.route('/enrollment', methods=['get', 'post'])
def enrollment():    
    # if user is not logged in, redirect to login page
    if not session.get('username'): 
        return redirect(url_for('login'))

    courseID    = request.form.get('courseID')
    courseTitle = request.form.get('title')  # same as get method above
    user_id     = session.get('user_id')  # get user_id from session

    if courseID:
        # use the model field name `courseID`
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops, you are already enrolled in this course {courseTitle}.", "danger")
            return redirect(url_for('courses'))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            print("-LEQUAN DEBUG-",Enrollment.user_id, Enrollment.courseID )
            flash(f"You have been enrolled in {courseTitle}!", "success")
            return redirect(url_for('courses'))

    classes = list( User.objects.aggregate(*[
                {
                    '$lookup': {
                        'from': 'enrollment', 
                        'localField': 'user_id', 
                        'foreignField': 'user_id', 
                        'as': 'r1'
                    }
                }, {
                    '$unwind': {
                        'path': '$r1', 
                        'includeArrayIndex': 'r1_id', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$lookup': {
                        'from': 'course', 
                        'localField': 'r1.courseID', 
                        'foreignField': 'courseID', 
                        'as': 'r2'
                    }
                }, {
                    '$unwind': {
                        'path': '$r2', 
                        'preserveNullAndEmptyArrays': False
                    }
                }, {
                    '$match': {
                        'user_id': user_id
                    }
                }, {
                    '$sort': {
                        'courseID': 1
                    }
                }
            ]))

    #term = request.form.get('term')

    return render_template('enrollment.html', enrollment=True, title="Enrollment", classes=classes)








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
    # clear username and user_id from session on logout
    session['username'] = None
    session.pop('user_id', None)
    return redirect(url_for('index'))           


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


@app.route('/delete_user')
def delete_user():
    # Delete user by email address
    email = "le_duc_quan@hotmail.com"
    user = User.objects(email=email).first()
    
    if user:
        user.delete()
        flash(f"User with email {email} has been deleted.", "success")
        return redirect(url_for('user'))
    else:
        flash(f"User with email {email} not found.", "danger")
        return redirect(url_for('user'))



