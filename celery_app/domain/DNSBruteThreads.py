# from dns import resolver
# from dns import rdatatype
# import threading
# import queue
# import re
# import os
# from app import pa_domain
#
#
#
# class DNSBruteThreads(threading.Thread):
#     #线程名,一级域名,二级域名队列
#     def __init__(self, thread_name, domain,subnames_queue):
#         super().__init__()
#         self.thread_name=thread_name
#         self.check_domain(domain)
#         self.subnames_queue=subnames_queue
#         self.subnames_exist_list=[]
#
#     #枚举子域名
#     def brute_dns(self):
#
#         while not self.subnames_queue.empty():
#             sub_name=self.subnames_queue.get()
#             #二级域名拼接
#             sub_domain=sub_name+'.'+self.domain
#             try:
#                 answer=resolver.query(sub_domain,rdatatype.A)
#                 #如果查询到了解析记录
#                 if answer:
#                     print("[+] " + sub_domain + " is exist")
#                     #收集子域名列表
#                     mylist.append(sub_domain)
#
#                 for data in answer:
#                     print(data)
#             except Exception as e:
#                 pass
#
#     #域名格式检查 输出类似 elong.com
#     def check_domain(self,domain):
#         #.的个数
#         point_num=len(re.findall("\.", domain))
#         #判断有gov.cn com.cn的情况
#         if len(re.findall("gov\.cn|com\.cn",domain))>0:
#             if point_num >2:
#                 print("传入的域名不合法，请检查")
#                 exit(0)
#             if point_num==2:
#                 self.domain = domain
#
#         if point_num ==1:
#             self.domain=domain
#         if point_num >1:
#             print("传入的域名不合法，请检查")
#             exit(0)
#
#     #将扫描出来的子域名进行存库
#     def save_sub_domain(self,domain,sub_domain_list):
#         pa_domain.update_one({"domain":domain},{domain:sub_domain_list})
#
#
#
#
#
#     def run(self):
#         self.brute_dns()
#
# def get_subnames_queue():
#     with open(os.path.dirname(__file__)+'/dict/test.txt', 'r') as f:
#         subnames_list=f.readlines()
#     length=len(subnames_list)
#     subnames_queue = queue.Queue(length)
#     for item in subnames_list:
#         subnames_queue.put(item.strip())
#     return subnames_queue
#
#
# #二级域名采集的主入口
# #参数是domain 待被采集的主域名
# def Brute_Sub_Domain(domain):
#     #获取domain
#     # domain=sys.argv[1]
#     # domain="baidu.com"
#
#     THREAD_NUM=20
#     threads=[]
#     #任务队列
#     subnames_queue=get_subnames_queue()
#
#
#     for i in range(THREAD_NUM):
#         thread=DNSBruteThreads("threading-"+str(i),domain,subnames_queue)
#         thread.start()
#         threads.append(thread)
#
#     for thread in threads:
#         thread.join()