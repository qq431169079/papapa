from flask import Blueprint,request
from app import pa_domain
from .tasks import scan_ip_task

ipscan_blueprint = Blueprint("ipscan", __name__, url_prefix='/ipscan')

#通过传入一个一级域名，对这个域名下的所有ip进行scan
@ipscan_blueprint.route('/scan')
def scan_ip():
    domain = request.args.get("domain")
    #在数据库搜索该domain的索引
    domain_index=pa_domain.find_one({"domain":domain})

    if domain_index:
        # 声明ip_list
        ip_list = []
        #获取整个domain所对应的ip
        for item in domain_index['subdomain']:
            for ip_s in item['ip']:
                ip_list.append(ip_s)
        #调用scan_ip 任务
        scan_ip_task.delay(ip_list)
        return {"code":200,"msg":"添加扫描任务成功"}

    return {"code":201,"msg":"未找到该域名所对应ip"}
