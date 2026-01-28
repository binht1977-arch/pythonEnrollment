import os

class Config(object):
    SECRET_KY = os.environ.get('SECRET_KEY') or 'secret_string for_dev'

    MONGODB_SETTINGS = {
        'db': 'UTA_Enrollment',
        'host': 'mongodb://localhost:27017/UTA_Enrollment',
        'port': 27017
    }