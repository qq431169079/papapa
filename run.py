
from app import create_app, make_celery


#创建Flask app实例
app = create_app('default')


#创建celery实例
celery=make_celery(app)

if __name__ == '__main__':
    app.run(debug=True)
