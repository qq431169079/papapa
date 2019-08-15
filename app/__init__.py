from flask import Flask
from celery_app import celery
from pymongo import MongoClient

#app
def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app.config)

    # 添加蓝本
    from celery_app.domainviews import domain_blueprint
    from celery_app.ipviews import ipscan_blueprint
    app.register_blueprint(domain_blueprint)
    app.register_blueprint(ipscan_blueprint)

    return app

#celery
def make_celery(app):
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


client = MongoClient("127.0.0.1", 27017,connect=False)
# 指定mongodb数据库
papapa = client.papapa
pa_domain=papapa.pa_domain
pa_sub_domain=papapa.pa_sub_domain
pa_ip=papapa.pa_ip


