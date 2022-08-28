from flask import Blueprint, render_template

error_pages = Blueprint('error_pages',__name__)


@error_pages.app_errorhandler(404)
def error_404(error):
    '''
    Error for pages not found.
    '''
    # Notice how we return a tuple!
    return render_template('error_pages/404.html'), 404


@error_pages.app_errorhandler(403)
def error_403(error):
    '''
    Error for trying to access something which is forbidden.
    Such as trying to update someone else's blog post.
    '''
    # return a tuple!
    return render_template('error_pages/403.html'), 403

@error_pages.app_errorhandler(409)
def error_409(error):
    '''
    Indicates that the request could not be processed because of
    conflict in the current state of the resource,
    such as an edit conflict between multiple simultaneous updates.
    '''
    # tuple!
    return render_template('error_pages/409.html'), 409
