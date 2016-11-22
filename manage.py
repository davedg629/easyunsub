#!/usr/bin/env python
import os
from app import create_app, db, admin
from app.models import User, Role, Session
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from flask_admin.contrib.sqla import ModelView


app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)
admin.add_view(ModelView(Role, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Session, db.session))


def make_shell_context():
    return dict(app=app, db=db, User=User,
                Role=Role, Session=Session
                )
manager.add_command("shell", Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
