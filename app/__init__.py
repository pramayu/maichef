from flask import Flask
from app.api import schema
from flask_graphql import GraphQLView
from flask_mongoengine import MongoEngine
from app.config.conf import DevelopmentConf
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
app.config.from_object(DevelopmentConf)
db = MongoEngine(app)

app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))