from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt ## password crypt 
from flask_login import LoginManager ## أهم حاجه
from flask_migrate import Migrate
from flask_ckeditor import CKEditor
from pythonic.config import Config
from flask_admin import Admin
# app = Flask(__name__)


## اساسى فى اى مشروع
# app.config.from_object(Config)
db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate(db)
ckeditor = CKEditor()
admin = Admin()
login_manager = LoginManager()
migrate = Migrate()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
# from pythonic.main.routes import main
# from pythonic.users.routes import users
# from pythonic.lessons.routes import lessons
# from pythonic.courses.routes import courses_bp
# app.register_blueprint(main)
# app.register_blueprint(users)
# app.register_blueprint(lessons)
# app.register_blueprint(courses_bp)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    from pythonic.adminbp.routes import MyAdminIndexView
    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    ckeditor.init_app(app)
    migrate.init_app(app,db)
    admin.init_app(app , index_view=MyAdminIndexView())
    
    

    from pythonic.main.routes import main
    from pythonic.users.routes import users
    from pythonic.lessons.routes import lessons
    from pythonic.courses.routes import courses_bp
    from pythonic.errors.handlers import errors
    from pythonic.adminbp.routes import adminbp

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(lessons)
    app.register_blueprint(courses_bp)
    app.register_blueprint(errors)
    app.register_blueprint(adminbp)

    with app.app_context():
        db.create_all()
        db.session.commit()

    return app
