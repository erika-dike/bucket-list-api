#!/usr/bin/env python
from flask.ext.script import Manager, prompt_bool, Server
from flask.ext.migrate import Migrate, MigrateCommand
from OpenSSL import SSL

from api.app import create_app
from api.models import User, BucketList, BucketListItem, db

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(ssl_context=('2_nazzyandfamz.com.crt', 'ssl.key')))


@manager.command
def create_db():
    """Creates database tables from sqlalchemy models"""
    db.create_all()


@manager.command
def drop_db():
    """Drops database tables"""
    if prompt_bool("Are you sure you want to lose all your data?"):
        db.drop_all()


@manager.shell
def make_shell_context():
    return dict(
        app=app, db=db, User=User,
        BucketList=BucketList,
        BucketListItem=BucketListItem
    )

if __name__ == '__main__':
    manager.run()
