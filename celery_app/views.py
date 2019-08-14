from flask import Blueprint,request
from .tasks import get_sub_domain_task
from app import pa_domain



celery_bp = Blueprint("domain", __name__, url_prefix='/celeryapp')



@celery_bp.route('/test')
def test():
    domain = request.args.get("domain")
    #如果域名已经添加过，就不需要添加了
    if(pa_domain.find_one({"domain":domain})):
        return {"code":201,"msg":"domain have added"}
    #添加域名
    pa_domain.insert_one({"domain":domain})
    # pa_domain.update_one({"domain":domain},{"$set":{"a":1}})
    #调用Cerely后台 进行子域名批量获取
    get_sub_domain_task.delay(domain)
    result={"code":200,"msg":"add success"}

    return result