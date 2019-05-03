from flask import Flask
from flask_migrate import Migrate, MigrateCommand
from flask_restful import Api
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy

from config import Configuration


app = Flask(__name__)
app.config.from_object(Configuration)

api = Api(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

from fleet.models import *
from user.models import *
from vehicle.models import *
