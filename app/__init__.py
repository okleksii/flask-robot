import werkzeug
from flask import Flask
from flask_migrate import Migrate
from dotenv import load_dotenv

from app.database import db

load_dotenv()

app = Flask(__name__)
app.config.from_pyfile("config.py")
db.init_app(app)
migrate = Migrate(app, db, render_as_batch=True)


@app.errorhandler(werkzeug.exceptions.NotFound)
def custom_404(exc):
    return "<h1>Custom 404</h1>", exc.code

