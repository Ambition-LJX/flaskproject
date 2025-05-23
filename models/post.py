from datetime import datetime
from exts import db
from sqlalchemy_serializer import SerializerMixin


class BoardModel(db.Model,SerializerMixin):
    serialize_only = ("id","name","priority","created_time")
    __tablename__ = 'board'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), unique=True)
    priority = db.Column(db.Integer, default=1)
    created_time = db.Column(db.DateTime, default=datetime.now)

# 帖子
class PostModel(db.Model,SerializerMixin):
    serialize_only = ("id","title","content","created_time","board","author")
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_time = db.Column(db.DateTime, default=datetime.now)

    # 创建外键
    board_id = db.Column(db.Integer, db.ForeignKey('board.id'))
    author_id = db.Column(db.String(100), db.ForeignKey('user.id'))

    board = db.relationship('BoardModel', backref=db.backref("posts"))  # BoardModel的对象 posts属性可以在BoardModel中调用
    author = db.relationship('UserModel', backref=db.backref("posts"))

# 轮播图
class BannerModel(db.Model,SerializerMixin):
    __tablename__ = 'banner'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    link_url = db.Column(db.String(255), nullable=False)
    priority = db.Column(db.Integer, default=0)
    create_time = db.Column(db.DateTime, default=datetime.now)

# 评论内容
class CommentModel(db.Model,SerializerMixin):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100), db.ForeignKey("user.id"), nullable=False)

    post = db.relationship("PostModel", backref=db.backref('comments', order_by="CommentModel.create_time.desc()", cascade="delete, delete-orphan"))
    author = db.relationship("UserModel", backref='comments')
