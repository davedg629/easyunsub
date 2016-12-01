from flask import render_template, url_for, redirect, flash, \
    current_app, session
from . import unsub
from flask_login import login_required, current_user
from .forms import UnsubForm, UnsubConfirmForm
from ..auth.decorators import public_endpoint
import praw
from .jobs import unsubscribe


@unsub.route('/unsub/', methods=['GET', 'POST'])
@login_required
@public_endpoint
def unsub_form():

    if 'subscribed' in session:
        subreddits = session['subscribed']
    else:
        r = praw.Reddit(
            client_id=current_app.config['REDDIT_APP_ID'],
            client_secret=current_app.config['REDDIT_APP_SECRET'],
            refresh_token=current_user.refresh_token,
            user_agent=current_app.config['REDDIT_USER_AGENT']
        )
        r.subreddit('easyunsub').subscribe()
        r.subreddit('easyunsub').unsubscribe()
        subscribed_subs = r.user.subreddits()
        subreddits = list()
        for sub in subscribed_subs:
            subreddits.append(sub.display_name)
    if subreddits:
        form = UnsubForm()
        form.subreddits.choices = [(x, x) for x in subreddits]

        if form.validate_on_submit():
            session['subreddits'] = form.subreddits.data
            return redirect(url_for('unsub.unsub_confirm'))

        session['subscribed'] = subreddits
        return render_template(
            'unsub/form.html',
            form=form,
            page_title=''
        )
    else:
        return render_template(
            'unsub/form.html',
            page_title=''
        )


@unsub.route('/unsub-confirm/', methods=['GET', 'POST'])
@login_required
@public_endpoint
def unsub_confirm():
    if 'subreddits' not in session:
        return redirect(url_for('unsub.unsub_form'))
    form = UnsubConfirmForm()
    if form.validate_on_submit():
        unsub_result = unsubscribe(
            current_user.id,
            session['subreddits'],
            current_app.config
        )
        if 'subscribed' in session:
            session.pop('subscribed', None)
        flash(unsub_result)
        return redirect(url_for('unsub.unsub_form'))
    return render_template(
        'unsub/confirm.html',
        subreddits=session['subreddits'],
        form=form,
        page_title=''
    )
