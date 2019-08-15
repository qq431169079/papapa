import os
import queue
import threading
from dns import resolver
from dns import rdatatype
from app import pa_domain,pa_sub_domain,pa_ip
from celery_app.utils.utils import get_current_time

class SubDomainBrute:
    def __init__(self,domain,threads_num):
        self.domain=domain
        self.threads_num=threads_num
        self.lock=threading.Lock()

        #生成my_resolver
        self.my_resolver = [resolver.Resolver() for _ in range(threads_num)]
        #获取本地的sub_names
        self.get_sub_names_queue()

        # 定义subdomain结果队列
        self.sub_domain_exist_result_queue = queue.Queue()
        # 定义subdomain列表
        self.sub_domain_exist_result_list = []


    #加载dns_servers,生成dns_servers_list
    def get_name_servers(self):
        with open(os.path.dirname(__file__)+'/dict/dns_servers.txt', 'r') as f:
            for line in f:
                if line:
                    self.dns_servers_list.append(line.strip())
        #给my_resolver 指定dns服务器
        self.my_resolver.nameservers=self.dns_servers_list


    def brute_domain(self):

        thread_id=int(threading.current_thread().name)
        #生成本线程的resolver
        my_resolver=self.my_resolver[thread_id]
        #设置DNS_服务器
        my_resolver.nameservers=['8.8.8.8','114.114.114.114']
        while self.sub_name_queue.qsize()>0:
            ip_temp=[]
            self.lock.acquire()
            #获取sub_name
            sub_name=self.sub_name_queue.get()
            self.lock.release()

            #拼接子域名
            sub_domain=sub_name+'.'+self.domain
            # 获取域名A记录
            try:
                answer=my_resolver.query(sub_domain,rdatatype.A)

                #如果查询到了解析记录
                if answer:
                    print("[+] " + sub_domain + " is exist")

                    #获取所有的A记录
                    for ip in answer:
                        ip_temp.append(ip.address)

                    # 结果推入queue中
                    self.lock.acquire()
                    self.sub_domain_exist_result_queue.put({"sub_domain":sub_domain,"ip":ip_temp})
                    self.lock.release()

            except Exception as e:
                pass

    # 加载sub_name,放进sub_name_queue队列中
    def get_sub_names_queue(self):
        self.sub_name_queue = queue.Queue()
        with open(os.path.dirname(__file__) + '/dict/test.txt', 'r') as f:
            for line in f:
                if line:
                    self.sub_name_queue.put(line.strip())


    #从文件里将结果取出来存进mongodb数据库
    def save_sub_domains(self):
        while not self.sub_domain_exist_result_queue.empty():
            self.sub_domain_exist_result_list.append(self.sub_domain_exist_result_queue.get())
        #去重存库 存入pa_domain
        pa_domain.update_one({"domain":self.domain},{"$set":{"subdomain":self.sub_domain_exist_result_list}})

        #存入二级域名
        for i in range(len(self.sub_domain_exist_result_list)):
            pa_sub_domain.insert({"subdomain":self.sub_domain_exist_result_list[i]['sub_domain']})
            for j in range(len(self.sub_domain_exist_result_list[i]['ip'])):
                # 存入ip
                #先判断数据库里有没有这个ip
                if not pa_ip.find_one({"ip":self.sub_domain_exist_result_list[i]['ip'][j]}):
                    pa_ip.insert({"ip":self.sub_domain_exist_result_list[i]['ip'][j],"has_scaned":False,"add_time":get_current_time(),"last_scan_time":""})



    def run(self):
        for i in range(self.threads_num):
            t = threading.Thread(target=self.brute_domain, name=str(i))
            t.setDaemon(True)
            t.start()
            t.join()

        self.save_sub_domains()


#程序的主入口
def sub_domain_brute(domain,thread_num):

    d=SubDomainBrute(domain,thread_num)
    d.run()

# sub_domain_brute('baidu.com',20)


