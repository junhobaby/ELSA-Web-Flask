from flask import Flask, render_template, abort
from models import db
from jinja2 import TemplateNotFound
from os import environ
from dotenv import load_dotenv
from blueprints.customers import customers_bp

load_dotenv()  # take environment variables from .env.

# GLOBAL VARIABLES
DB_USER = environ.get('DB_USER', 'postgres')
DB_PASSWORD = environ.get('DB_PASSWORD', None)
DB_HOST = environ.get('DB_HOST', None)
DB_NAME = environ.get('DB_NAME', None)
DB_PORT = environ.get('DB_PORT', None)
DB_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

# FLASK CONFIGURATION
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # removes warning of significant overhead for Flask SQLAlchemy
app.debug = True

# DATABASE CONNECTION
db.init_app(app)

# BLUEPRINT REGISTRATION
app.register_blueprint(customers_bp)


@app.route('/', defaults={'page': 'home'})
@app.route('/<page>')
def show(page):
    try:
        return render_template(f'pages/{page}.html')
    except TemplateNotFound:
        abort(404)


if __name__ == '__main__':
    app.run()
