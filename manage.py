import unittest
import coverage

from flask_script import Manager
from flask_migrate import MigrateCommand

from users import create_app, db
from users.models import User


COV = coverage.coverage(
    branch=True,
    include='users/*',
    omit=[
        'users/tests/*'
    ]
)
COV.start()


app = create_app()
app.app_context().push()
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('admin/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@manager.command
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('admin/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1


@manager.command
def recreate_db():
    """Recreates a database."""
    db.drop_all()
    db.create_all()
    db.session.commit()


@manager.command
def seed_db():
    """Seeds the database."""
    db.session.add(User(
        username='guidocecilio',
        email='guidocecilio@gmail.com',
        password='test'
    ))
    db.session.add(User(
        username='guidoenmanuel',
        email='guidoenmanuel@gmail.com',
        password='test'
    ))
    db.session.commit()


if __name__ == '__main__':
    manager.run()