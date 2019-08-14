
from app import create_app, make_celery
from celery_app.views import celery_bp

#创建Flask app实例
app = create_app('default')
#添加程序的蓝本
app.register_blueprint(celery_bp)

#创建celery实例
celery=make_celery(app)

if __name__ == '__main__':
    app.run(debug=True)
