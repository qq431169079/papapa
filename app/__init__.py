from flask import Flask
from celery_app import celery
from pymongo import MongoClient

#app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app.config)

    # 添加蓝本
    from celery_app.views import celery_bp
    app.register_blueprint(celery_bp)

    return app

#celery
def make_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


client = MongoClient("127.0.0.1", 27017)
# 指定mongodb数据库
papapa = client.papapa
pa_domain=papapa.pa_domain


