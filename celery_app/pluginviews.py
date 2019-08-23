from flask import Blueprint,request
from .tasks import check_plugins_task
import importlib


pluginscan_blueprint = Blueprint("pluginscan", __name__, url_prefix='/pluginscan')

@pluginscan_blueprint.route('/scan',methods=['GET', 'POST'])
def plugins_scan():
    if request.method=="POST":
        json_data=request.get_json()
        plugins_id_list=json_data['plugins_id_list']
        domains_list=json_data['domains_list']
        # 调用celery任务
        check_plugins_task.delay(plugins_id_list,domains_list)
        return {"code": 200, "msg": "plugin scan task success"}

    return {"code": 201, "msg": "POST method need"}

