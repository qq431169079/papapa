
from . import celery
from .domain.SubDomainBrute import sub_domain_brute

#Celery 爆破子域名任务
@celery.task()
def get_sub_domain_task(domain):
    print("get_sub_domain.task start")
    sub_domain_brute(domain,20)
    print("get_sub_domain.task end")
    return True


#对ip进行扫描，扫描相应的端口，已经服务
@celery.task()
def scan_ip_task(ip_list):
    print("get_sub_domain.task start")
    print(ip_list)
    print("get_sub_domain.task end")
    return True



