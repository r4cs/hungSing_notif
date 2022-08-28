 # notificadorHSproject/__init__.py

import os
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


app = Flask(__name__)

mail = Mail(app)


####################################################################
############ CONFIGURATIONS (MORE IN CONFIG.PY FILE) ###############
###################################################################
# Remember is needed to set the environment variables at the command line
# when deploying this.
# export SECRET_KEY=mysecret
# set SECRET_KEY=mysecret # windows #

app.config.from_object(os.environ.get('APP_SETTINGS'))
# print(os.environ['APP_SETTINGS']) ## prints: config.ProductionConfig

# #################################
# ### DATABASE SETUPS ############
# ###############################

db = SQLAlchemy(app)

migrate = Migrate(app, db)

###########################
#### LOGIN CONFIGS #######
#########################

login_manager = LoginManager()

# We can now pass in our app to the login manager
login_manager.init_app(app)

# Tell users what view to go to when they need to login.
login_manager.login_view = "users.login"
login_manager.session_protection = "strong"
login_manager.refresh_view = "users.login"
login_manager.needs_refresh_message = (
    u"Para proteger sua conta, por favor faça login novamente"
)
login_manager.needs_refresh_message_category = "info"


###########################
#### BLUEPRINT CONFIGS ####
##########################

# Import these at the top if you want
# We've imported them here for easy reference
from notificadorHSproject.users.views import users
from notificadorHSproject.core.views import core
from notificadorHSproject.error_pages.handlers import error_pages

# Register the apps
app.register_blueprint(users)
app.register_blueprint(core)
app.register_blueprint(error_pages)