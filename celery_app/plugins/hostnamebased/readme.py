import requests
from app import pa_vuln
from celery_app.utils.utils import get_current_time

#readme 插件 用来检测http协议和https协议是否存在readme文件，返回的是一个列表，第一个元素是http的结果，第二个是https的
#如果2个协议都没有漏洞的话返回[False,False]
#如果都有的话是[(True,主机,内容),(True,主机,内容)]

headers={"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36"}

def check(host):
    result = []
    uris = ['readme.md', 'README.MD', 'readme.MD', 'README.md']

    schemes=['http','https']
    result_http=False
    result_https=False

    for scheme in schemes:

        target = "{0}://{1}/".format(scheme, host)

        try:
            for uri in uris:
                url=target+uri
                requests.packages.urllib3.disable_warnings()
                response=requests.get(url,headers=headers,verify=False)
                if response.status_code == 200 and response.headers.get('Content-Type') in ['application/octet-stream','text/markdown']:
                    if len(response.text) and response.text[0] not in ['<','{','[']:
                        output=response.text
                        if scheme=='http':
                            result_http=(True,scheme,host,url,output)
                        if scheme=='https':
                            result_https = (True, scheme,host,url,output)

        except Exception as e:
            pass

    result.append(result_http)
    result.append(result_https)

    #入库
    if len(result)>0:
        for info in result:
            if info:
                pa_vuln.insert({"host":info[2],"vuln_proof":info[4],"vuln_url":info[3],"plugin_id":1,"plugin_info":"用来探测网站是否存在readme文件","add_time":get_current_time()})
    return result


print(check("check.newmine.net"))

