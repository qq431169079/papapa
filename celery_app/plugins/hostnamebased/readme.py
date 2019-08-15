import requests




def check(host,port):
    scheme='http'
    if port==443:
        scheme='https'
    target="{0}://{1}:{2}/".format(scheme,host,port)
    uris=['readme.md','README.MD','readme.MD','README.md']


    try:
        for uri in uris:
            url=target+uri

            response=requests.get(url)
            if response.status_code == 200 and response.headers.get('Content-Type') in ['application/octet-stream','text/markdown']:
                if len(response.text) and response.text[0] not in ['<','{','[']:
                    output=response.text
                    return True,host,port,output

    except Exception as e:
        return False

    return False





