
from . import celery
from .domain.SubDomainBrute import sub_domain_brute

#Celery 爆破子域名任务
@celery.task()
def get_sub_domain_task(domain):
    print("get_sub_domain.task start")
    sub_domain_brute(domain,10)
    print("get_sub_domain.task end")
    return True



