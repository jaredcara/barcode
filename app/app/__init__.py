from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bootstrap import Bootstrap

from config import Config

#   Initalize flask and the SQLAchemy datbase.
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

#   Initalize bootstrap
bootstrap = Bootstrap(app)

#   Enable database migration.
migrate = Migrate(app, db)

#   Import models last for the database.
from app import routes, models, errors

