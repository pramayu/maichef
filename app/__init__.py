from flask import Flask
from flask_mongoengine import MongoEngine
from app.config.conf import DevelopmentConf

app = Flask(__name__)
app.config.from_object(DevelopmentConf)
db = MongoEngine(app)