from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets
from flask_caching import Cache

db = SQLAlchemy()
cache = Cache(config={'CACHE_TYPE': 'RedisCache',
                      'CACHE_REDIS_HOST': '0.0.0.0',
                      'CACHE_REDIS_PORT': 6379})

app = Flask(__name__)
cache.init_app(app)

app.config['SECRET_KEY'] = secrets.token_hex(16)

POSTGRES = {
    'user': 'postgres',
    'pw': 'new_password',
    'db': 'my_food_blog',
    'host': 'localhost',
    'port': '5432',
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

from .models import User

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# blueprint for auth routes in our app
from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from .main import main as main_blueprint
app.register_blueprint(main_blueprint)

from .dashboard import bp as dashboard_blueprint
app.register_blueprint(dashboard_blueprint)

if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
