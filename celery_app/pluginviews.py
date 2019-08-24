from flask import Blueprint,request
from .tasks import check_plugins_task
from app import pa_domain,pa_taskid
from celery_app.utils.utils import get_current_time


pluginscan_blueprint = Blueprint("pluginscan", __name__, url_prefix='/pluginscan')

@pluginscan_blueprint.route('/scan',methods=['POST'])
#传入一个插件id的列表，一个二级域名的列表，开始对每一个二级域名进行每一个插件的扫描
def plugins_scan_by_subdomain():
    if request.method=="POST":
        json_data=request.get_json()
        plugins_id_list=json_data['plugins_id_list']
        domains_list=json_data['domains_list']
        # 调用celery任务
        check_plugins_task.delay(plugins_id_list,domains_list)
        return {"code": 200, "msg": "plugin scan task success"}


#传入一个一级域名，对数据库内该一级域名的所有二级域名进行每一个插件的扫描
@pluginscan_blueprint.route('/scanbydomain',methods=['POST'])
def plggins_scan_by_maindomain():
    if request.method=="POST":
        #获取POST过来的数据
        json_data = request.get_json()
        plugins_id_list = json_data['plugins_id_list']
        domain = json_data['domain']
        #声明二级域名的列表

        subdomain_list=[]
        #通过domain获取所有的该domain的二级域名
        index=pa_domain.find_one({"domain":domain})
        if index:
            subdomain=index['subdomain']
            for sub in subdomain:
                subdomain_list.append(sub["sub_domain"])
        #没有在数据库中找到该主域名
        else:
            return {"code": 202, "msg": "did not find domain {0}".format(domain)}

        if len(subdomain_list)>0:
            # 调用celery任务,并且获取任务id
            r=check_plugins_task.delay(plugins_id_list, subdomain_list)
            #记录任务id
            pa_taskid.insert({"task_id":r.task_id,"add_time":get_current_time(),"task_info":"对{0}等域名进行插件扫描".format(subdomain_list[0])})


        return {"code": 200, "msg": "plugin scan task success"}
    return {"code": 201, "msg": "POST method need"}







