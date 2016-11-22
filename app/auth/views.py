from flask import render_template, url_for, flash, redirect, \
    session, current_app, request, g
from . import auth
from .. import db
from flask_login import logout_user, login_user, login_required, \
    current_user
from ..models import User
from .utils import generate_token
from .decorators import admin_login_required, public_endpoint
from .forms import LoginForm
import praw


@auth.before_app_request
def before_request():
    login_valid = 'logged_in' in session
    if login_valid:
        if current_user.is_authenticated:
            g.user = current_user
        else:
            g.user = None
    elif (request.endpoint and
          'static' not in request.endpoint and
          not login_valid and
          not getattr(
              current_app.view_functions[request.endpoint],
              'is_public',
              False)
          ):
        return redirect(url_for('auth.admin_login'))


# admin logout
@auth.route('/admin-logout/')
@admin_login_required
def admin_logout():
    session.pop('logged_in', None)
    flash('You have logged out of the admin account.')
    return redirect(url_for('main.index'))


# admin login
@auth.route('/admin-login/', methods=['GET', 'POST'])
@public_endpoint
def admin_login():
    if 'logged_in' in session:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        if request.form['username'] == \
                current_app.config['ADMIN_USERNAME'] and \
                request.form['password'] == \
                current_app.config['ADMIN_PASSWORD']:
            session['logged_in'] = True
            flash('Admin login successful.')
            return redirect(url_for('admin.index'))
        else:
            flash('Invalid username or password.')
            return redirect(url_for('auth.admin_login'))
    return render_template(
        'auth/admin_login.html',
        page_title='Admin Login',
        form=form
    )


# reddit logout
@auth.route('/logout')
@login_required
@public_endpoint
def logout():
    logout_user()
    flash('You have been logged out of your Reddit account.')
    return redirect(url_for('main.index'))


# reddit login
@auth.route("/login")
@public_endpoint
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    r = praw.Reddit(user_agent=current_app.config['REDDIT_USER_AGENT'])
    r.set_oauth_app_info(
        current_app.config['REDDIT_APP_ID'],
        current_app.config['REDDIT_APP_SECRET'],
        current_app.config['OAUTH_REDIRECT_URI']
    )
    session['oauth_token'] = generate_token()
    oauth_link = r.get_authorize_url(
        session['oauth_token'],
        ['identity', 'subscribe', 'mysubreddits'],
        True
    )
    return render_template(
        'auth/login.html',
        page_title="Easily Unsubscribe from Subreddits",
        oauth_link=oauth_link
    )


# reddit authorize
@auth.route('/authorize/')
@public_endpoint
def authorize():
    state = request.args.get('state', '')
    if current_user.is_anonymous and (state == session['oauth_token']):
        try:
            code = request.args.get('code', '')
            r = praw.Reddit(user_agent=current_app.config['REDDIT_USER_AGENT'])
            r.set_oauth_app_info(
                current_app.config['REDDIT_APP_ID'],
                current_app.config['REDDIT_APP_SECRET'],
                current_app.config['OAUTH_REDIRECT_URI']
            )
            access_info = r.get_access_information(code)
            user_reddit = r.get_me()
            user = User.query\
                .filter_by(username=user_reddit.name)\
                .first()
            if user is None:
                user = User(
                    username=user_reddit.name,
                    role_id=2,
                    refresh_token=access_info['refresh_token']
                )
                db.session.add(user)
                db.session.commit()
            else:
                user.refresh_token = access_info['refresh_token']
                db.session.commit()
            login_user(user)
            if 'subscribed' in session:
                session.pop('subscribed', None)
            flash('Hi /u/' + user.username + '! You have successfully' +
                  ' logged in with your reddit account.')
            return redirect(url_for('main.index'))
        except praw.errors.OAuthException:
            flash('There was a problem with your login. Please try again.')
            return redirect(url_for('auth.login'))
    else:
        return redirect(url_for('auth.login'))
