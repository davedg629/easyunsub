from flask import redirect, url_for, render_template
from . import main
from flask_login import current_user
from ..auth.decorators import public_endpoint


@main.route('/')
@public_endpoint
def index():
    if current_user.is_authenticated:
        return redirect(url_for('unsub.unsub_form'))
    else:
        return redirect(url_for('auth.login'))


@main.route('/about/')
@public_endpoint
def about():
    return render_template(
        'main/about.html',
        page_title='About EasyUnsub'
    )
