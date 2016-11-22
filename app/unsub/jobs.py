from flask import flash
import os
from app import create_app
import praw
from app.models import User


def unsubscribe(user_id, subreddits):

    app = create_app(os.getenv('FLASK_CONFIG') or 'default')
    with app.app_context():

        try:
            user = User.query\
                .filter_by(id=user_id)\
                .first()
            r = praw.Reddit(user_agent=app.config['REDDIT_USER_AGENT'])
            r.set_oauth_app_info(
                app.config['REDDIT_APP_ID'],
                app.config['REDDIT_APP_SECRET'],
                app.config['OAUTH_REDIRECT_URI']
            )
            r.refresh_access_information(user.refresh_token)
            unsubbed = list()
            flash_msg = 'You have been unsubscribed' + \
                ' from the following subreddits: '
            lcv = 1
            for sub in subreddits:
                r.get_subreddit(sub).unsubscribe()
                unsubbed.append(sub)
                if lcv == len(subreddits):
                    flash_msg = flash_msg + '/r/' + sub
                else:
                    flash_msg = flash_msg + '/r/' + sub + ', '

            return flash_msg

        except praw.errors.APIException as e:
            return e.message

        except praw.errors.ClientException as e:
            return e.message
