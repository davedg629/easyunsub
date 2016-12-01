import praw
from app.models import User


def unsubscribe(user_id, subreddits, config):
    user = User.query\
        .filter_by(id=user_id)\
        .first()
    r = praw.Reddit(
        client_id=config['REDDIT_APP_ID'],
        client_secret=config['REDDIT_APP_SECRET'],
        refresh_token=user.refresh_token,
        user_agent=config['REDDIT_USER_AGENT']
    )
    if len(subreddits) > 1:
        print subreddits[1:]
        r.subreddit(subreddits[0]).unsubscribe(subreddits[1:])
    else:
        r.subreddit(subreddits[0]).unsubscribe()
    flash_msg = 'You have been unsubscribed' + \
        ' from the following subreddits: '
    lcv = 1
    for sub in subreddits:
        if lcv == len(subreddits):
            flash_msg = flash_msg + '/r/' + sub
        else:
            flash_msg = flash_msg + '/r/' + sub + ', '

    return flash_msg
