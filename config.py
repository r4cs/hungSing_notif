import os
from notificadorHSproject import app
from datetime import timedelta
# OBS:

# os.environ.get('') => localiza pela value daqui, que tb eh key quando em exports, ex:
#    os.environ.get('APP_MAIL_USERNAME') retorna 'n0t1f1c4d0r'
#    os.environ.get('MAIL_USERNAME') n retrona nada
#
# app.config[''] => localiza pela key do script, ex:
#    app.config['MAIL_USERNAME'] retorna 'n0t1f1c4d0r'
#     app.config['APP_MAIL_USERNAME'] retorna KeyError


class BaseConfig(object):
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['PASSWORD_SALT'] = os.environ.get('SECURITY_PASSWORD_SALT')
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5) # (minutes=5)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(minutes=5) # (minutes=5)


    # mail settings
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465

    # # gmail authentication
    app.config['MAIL_USERNAME'] = os.environ.get('APP_MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('APP_MAIL_PASSWORD')
    # mail account
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get("MAIL_DEFAULT_SENDER")



class ProductionConfig(BaseConfig):
    DEBUG = True


class StagingConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(BaseConfig):
    DEVELOPMENT = True
    DEBUG = True
