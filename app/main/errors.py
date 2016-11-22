from flask import render_template
from . import main


@main.app_errorhandler(404)
def page_not_found(e):
    return render_template(
        '404.html',
        page_title='Page Not Found'
    ), 404


@main.app_errorhandler(500)
def internal_server_error(e):
    return render_template(
        '500.html',
        page_title='Error!'
    ), 500


@main.app_errorhandler(403)
def access_denied(e):
    return render_template(
        '403.html',
        page_title='Access Denied'
    ), 403
