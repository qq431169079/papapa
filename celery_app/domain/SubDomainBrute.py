import os
import queue
import threading
from dns import resolver
from dns import rdatatype
from app import pa_domain,papapa

#定义subdomain结果队列
sub_domain_exist_result_queue=queue.Queue()
#定义subdomain列表
sub_domain_exist_result_list=[]


class SubDomainBrute:
    def __init__(self,domain,threads_num):
        self.domain=domain
        self.threads_num=threads_num
        self.sub_name_queue=queue.Queue()
        self.lock=threading.Lock()
        #获取本地的sub_names
        self.get_sub_names()




    #加载sub_name,放进sub_name_queue队列中
    def get_sub_names(self):
        with open(os.path.dirname(__file__)+'/dict/test.txt', 'r') as f:
            for line in f:
                if line:
                    self.sub_name_queue.put(line.strip())


    def brute_domain(self):
        while not self.sub_name_queue.empty():
            #获取sub_name
            sub_name=self.sub_name_queue.get()
            #拼接子域名
            sub_domain=sub_name+'.'+self.domain
            #获取域名A记录
            try:
                answer=resolver.query(sub_domain,rdatatype.A)
                #如果查询到了解析记录
                if answer:
                    print("[+] " + sub_domain + " is exist")
                    #结果推入queue中
                    self.lock.acquire()
                    sub_domain_exist_result_queue.put(sub_domain)
                    self.lock.release()

                for data in answer:
                    print(data)

            except Exception as e:
                print(e)




    def run(self):
        for i in range(self.threads_num):
            t = threading.Thread(target=self.brute_domain(), name='thread-'+str(i))
            t.setDaemon(True)
            t.start()


#从文件里将结果取出来存进mongodb数据库
def save_sub_domains(domain):
    while not sub_domain_exist_result_queue.empty():
        sub_domain_exist_result_list.append(sub_domain_exist_result_queue.get())
    pa_domain.update_one({"domain":domain},{"$set":{"subdomain":sub_domain_exist_result_list}})




#程序的主入口
def sub_domain_brute(domain,thread_num):
    d=SubDomainBrute(domain,thread_num)
    d.run()
    save_sub_domains(domain)








