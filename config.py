import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'W\x02\xa7Q\xa0y\x84\x90.k\x8b\xcdm\xb3\xcco'

    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment',
        'host': 'mongodb://localhost:27017/UTA_Enrollment',
        'port': 27017
    }