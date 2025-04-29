from flask_mail import Message
from exts import mail
from celery import Celery

# 定义任务函数
def send_mail(recipient, subject, body): # 接受者 主题 内容
    message = Message(subject, recipients=[recipient],body=body)
    try:
        mail.send(message)
        return {"status": "SUCCESS"}
    except Exception as e:
        print(e)
        return {"status": "FAIL"}


# 创建celer对象工厂函数
def make_celery(app):
    celery=Celery(app.import_name,backend=app.config['CELERY_RESULT_BACKEND'],
                  broker=app.config['CELERY_BROKER_URL'])
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    app.celery = celery

    # 添加任务
    celery.task(name="send_mail")(send_mail)

    return celery

