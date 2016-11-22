from flask import render_template, url_for, redirect, flash, \
    current_app, session
from .. import q
from . import unsub
from flask_login import login_required, current_user
from .forms import UnsubForm, UnsubConfirmForm
from ..auth.decorators import public_endpoint
import praw
from .jobs import unsubscribe
from rq.job import Job
from ..worker import conn


@unsub.route('/unsub/', methods=['GET', 'POST'])
@login_required
@public_endpoint
def unsub_form():

    if 'subscribed' in session:
        subreddits = session['subscribed']
    else:
        r = praw.Reddit(user_agent=current_app.config['REDDIT_USER_AGENT'])
        r.set_oauth_app_info(
            current_app.config['REDDIT_APP_ID'],
            current_app.config['REDDIT_APP_SECRET'],
            current_app.config['OAUTH_REDIRECT_URI']
        )
        r.refresh_access_information(current_user.refresh_token)
        subscribed_subs = r.get_my_subreddits(limit=500)
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
        job = q.enqueue_call(
            func=unsubscribe,
            args=(current_user.id, session['subreddits']),
            result_ttl=5000
        )
        return redirect(url_for('unsub.loading', job_id=job.get_id()))
    return render_template(
        'unsub/confirm.html',
        subreddits=session['subreddits'],
        form=form,
        page_title=''
    )


@unsub.route('/loading/<job_id>', methods=['GET'])
@login_required
@public_endpoint
def loading(job_id):
    if 'subscribed' in session:
        session.pop('subscribed', None)
    return render_template(
        'unsub/loading.html',
        page_title='Unsubscribing...'
    )


@unsub.route('/status/<job_key>', methods=['GET'])
@login_required
@public_endpoint
def check_status(job_key):
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
        flash(job.result)
        return str(job.result), 200
    else:
        return "Nay!", 202
