from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config
from app.utils.helpers import register_error_handlers, register_template_filters, register_context_processors

# 初始化扩展
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'


def create_app(config_name='default'):
    # 创建并配置应用
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    # 使用应用初始化扩展
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # 注册蓝图
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.routes.news import news as news_blueprint
    app.register_blueprint(news_blueprint)

    # 注册错误处理器、模板过滤器和上下文处理器
    register_error_handlers(app)
    register_template_filters(app)
    register_context_processors(app)

    # 如果数据库表不存在则创建
    with app.app_context():
        db.create_all()

    return app
