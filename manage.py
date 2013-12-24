import os
from flask.ext import script
from animeta import app, db

manager = script.Manager(app)

# Override the default `runserver` command, to monitor the change of
# the configuration file.
# XXX: `Config.root_path` is an undocumented attribute.
config_path = os.path.join(app.config.root_path, 'config.py')
runserver = script.Server(extra_files=[config_path])
manager.add_command('runserver', runserver)


db_manager = script.Manager()

@db_manager.command
def create_all():
    db.create_all()

@db_manager.command
def drop_all():
    if script.prompt_bool('This action will DESTROY ALL DATA. Continue'):
        db.drop_all()

manager.add_command('db', db_manager)


if __name__ == '__main__':
    manager.run()
