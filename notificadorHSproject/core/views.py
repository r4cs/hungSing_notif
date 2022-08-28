# notificadorHSproject/core/views.py

from flask import render_template,request,Blueprint

core = Blueprint('core',__name__)

@core.route('/')
def index():
    '''
    This is the home page view.
    '''
    return render_template('index.html')
