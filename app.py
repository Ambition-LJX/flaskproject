from flask import Flask, send_from_directory
from flask_migrate import Migrate
import logging

import commands
import config
from apps.cmsapi import cmsapi_bp
from apps.front import front_bp
from apps.media import media_bp
from bbs_celery import make_celery
from exts import db, mail, cache, csrf, avatars, jwt, cors
import os

app = Flask(__name__)
app.config.from_object(config)

# 配置日志级别
app.logger.setLevel(logging.ERROR)  # 只显示错误级别的日志
logging.getLogger('werkzeug').setLevel(logging.ERROR)  # 设置 werkzeug 日志级别

# 初始化扩展
db.init_app(app)
mail.init_app(app)
cache.init_app(app)
csrf.init_app(app)
avatars.init_app(app)
jwt.init_app(app)

# 正确配置 CORS（在注册蓝图前）
cors.init_app(
    app,
    resources={
        r"/cmsapi/.*": {  # 匹配所有以 /cmsapi 开头的路径
            "origins": "http://127.0.0.1:8080",
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization", "Content-Disposition"],
            "expose_headers": ["Content-Disposition"],
            "supports_credentials": True  # 允许凭据
        }
    }
)

# 排除 CSRF 验证
csrf.exempt(cmsapi_bp)

migrate = Migrate(app, db)
mycelery = make_celery(app)

# 注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)
app.register_blueprint(cmsapi_bp)

# 注册命令
app.cli.command("init_boards")(commands.init_boards)
app.cli.command("create_test_posts")(commands.create_test_posts)
app.cli.command("init_roles")(commands.init_roles)
app.cli.command("bind_roles")(commands.bind_roles)

if __name__ == '__main__':
    app.run(debug=False, port=8200)  # 关闭调试模式