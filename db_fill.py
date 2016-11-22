import os
from app import create_app, db
from app.models import User, Role


app = create_app(os.getenv('FLASK_CONFIG') or 'default')

with app.app_context():

    db.session.add(
        Role(
            name='Admin'
        )
    )

    db.session.add(
        Role(
            name='User'
        )
    )

    db.session.add(
        User(
            username="groupsrc",
            role_id=1
        )
    )

    db.session.commit()
