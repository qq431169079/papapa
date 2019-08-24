
from . import celery
from .domain.SubDomainBrute import sub_domain_brute
from app import pa_plugin
import importlib

PLUGIN_DIR="celery_app.plugins.hostnamebased"

#Celery 爆破子域名任务
@celery.task()
def get_sub_domain_task(domain):
    print("get_sub_domain.task start")
    sub_domain_brute(domain,20)
    print("get_sub_domain.task end")
    return True


#对ip进行扫描，扫描相应的端口，以及服务
@celery.task()
def scan_ip_task(ip_list):
    print("scan_ip.task start")
    print(ip_list)
    print("scan_ip.task end")
    return True

#对选取的插件和domain进行检测
@celery.task()
def check_plugins_task(plugins_id_list,domains_list):
    print("check_plugins.task start")
    for domain in domains_list:
        for plugin_id in plugins_id_list:
            pa_plugin_index=pa_plugin.find_one({"plugin_id":plugin_id})
            if pa_plugin_index:
                plugin_name=pa_plugin_index["plugin_name"]
                plugin_module=importlib.import_module("{0}.{1}".format(PLUGIN_DIR,plugin_name))
                plugin_module.check(host=domain)

    print("check_plugins.task end")
    return True















