from application import app 
from flask import render_template
from flask import request, json, Response

courseData = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route('/')
@app.route('/index')
@app.route('/home')
def index():
    return render_template('index.html',index=True)

@app.route('/login')
def login():           
    return render_template('login.html',index=True)            


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



