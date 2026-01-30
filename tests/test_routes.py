import pytest

from application import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Disable CSRF checks for form posts in tests
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        yield client


def test_app_importable():
    assert app is not None


def test_index(client):
    rv = client.get('/')
    assert rv.status_code == 200
    assert b'Welcome to Universal Tech Academy.' in rv.data


def test_login_get(client):
    rv = client.get('/login')
    assert rv.status_code == 200
    assert b'<h1>Login</h1>' in rv.data


def test_login_post_success(client):
    # Successful login should redirect to index
    rv = client.post('/login', data={'email': 'le_duc_quan@hotmail.com', 'password': 'password123'}, follow_redirects=False)
    assert rv.status_code in (302, 303)
    # Follow redirect and verify landing page content
    rv2 = client.post('/login', data={'email': 'le_duc_quan@hotmail.com', 'password': 'password123'}, follow_redirects=True)
    assert rv2.status_code == 200
    assert b'Welcome to Universal Tech Academy.' in rv2.data


def test_courses_page(client):
    rv = client.get('/courses/')
    assert rv.status_code == 200
    assert b'Course Offerings' in rv.data


def test_api_all(client):
    rv = client.get('/api/')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, list)
    assert 'courseID' in data[0]


def test_api_item(client):
    rv = client.get('/api/0')
    assert rv.status_code == 200
    data = rv.get_json()
    assert isinstance(data, dict)
    assert data.get('courseID') == '1111'


def test_enrollment_post(client):
    rv = client.post('/enrollment', data={'courseID': '9999', 'title': 'Test Course', 'term': 'Fall 2026'}, follow_redirects=True)
    assert rv.status_code == 200
    assert b'Test Course' in rv.data
