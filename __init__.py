from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.unpackaged.config import Config

# url_for is used in layout header to specify link to css
app = Flask(__name__)
app.config.from_object(Config)
# this var will be used in home.html body

# to generate secret key we can import secrets, then secrets.token_hex(16) in interpreter
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.login'
# adds blue box around the message because info is bootstrap
login_manager.login_message_category = 'info'

mail = Mail(app)

from flaskblog.users.routes import users
from flaskblog.posts.routes import posts
from flaskblog.main.routes import main
from flaskblog.errors.handlers import errors

app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)
app.register_blueprint(errors)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    # errors is instance of blueprint in handlers.py
    from flaskblog.errors.handlers import errors
    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)
    app.register_blueprint(errors)

    return app