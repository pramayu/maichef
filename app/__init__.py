from flask import Flask
from app.config.conf import DevelopmentConf

app = Flask(__name__)
app.config.from_object(DevelopmentConf)