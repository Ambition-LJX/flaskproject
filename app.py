from flask import Flask
from flask_migrate import Migrate

import commands
import config
from apps.cmsapi import cmsapi_bp
from apps.front import front_bp
from apps.media import media_bp

from exts import db, mail, cache, csrf, avatars, jwt, cors

app = Flask(__name__)
app.config.from_object(config)

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

# 注册蓝图
app.register_blueprint(front_bp)
app.register_blueprint(media_bp)
app.register_blueprint(cmsapi_bp)

# 注册命令
app.cli.command("init_boards")(commands.init_boards)
app.cli.command("init_roles")(commands.init_roles)
app.cli.command("init_developor")(commands.init_developor)
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=False, port=8200)  # 关闭调试模式