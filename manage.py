 
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import db, create_app
from dotenv import load_dotenv
import unittest

# loading env variables
load_dotenv()

# initialize the app with all its configurations
app = create_app(config_name=os.getenv('APP_SETTINGS'))
migrate = Migrate(app, db)

# create an instance of class that will handle our commands
manager = Manager(app)


# migration command
# usage
# python manage.py db init/migrate/upgrade
manager.add_command('db', MigrateCommand)

# load test with manager
# usage
# python manage.py test

@manager.command
def test():
    tests = unittest.TestLoader().discover('./tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1
    
if __name__ == '__main__':
    manager.run()

