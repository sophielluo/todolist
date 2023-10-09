from flask import Flask
#.extensions implies that it is on the same level as curr file
from .extensions import db, login_manager
from .models import User
from .routes import main



def create_app(database_uri="sqlite:///db.sqlite3"):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    #app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite://user:pass@localhost:5000/todolist"
    app.config["SECRET_KEY"] = "c4898b0f3886ab94e8d78b02"
    # https://stackoverflow.com/questions/34902378/where-do-i-get-secret-key-for-flask
    # used to sign session cookies for protection against cookie data tampering
    app.config['UPLOAD_FOLDER'] = 'project/uploads'

    db.init_app(app)
    # with app.app_context():
    #     db.create_all()
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    app.register_blueprint(main)
    return app