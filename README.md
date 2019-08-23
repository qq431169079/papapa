## papapa
一款用于资产发现和批量poc探测的扫描器

### 搭建方法
- 首先启动redis
 
```
redis-server
```

- 启动mongodb

```
 mongod --dbpath ../../data/db
```

- 在项目目录下启动celery

```
papapa_venv/bin/celery worker -A run.celery --loglevel=info
``` 
![](http://tiaogithub.cn-bj.ufileos.com/papapa03.png)

### mongoDB数据库Collection
#### papapa数据库建立以下集合

- pa_domain
- pa_ip
- pa_plugin
- pa_sub_domain
- pa_urls
- pa_vuln

### 项目目录结构

```
├── README.md
├── __pycache__
│   └── run.cpython-36.pyc
├── app
│   ├── __init__.py
│   └── __pycache__
│       └── __init__.cpython-36.pyc
├── celery_app  
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-36.pyc
│   │   ├── domainviews.cpython-36.pyc
│   │   ├── ipviews.cpython-36.pyc
│   │   ├── pluginviews.cpython-36.pyc
│   │   └── tasks.cpython-36.pyc
│   ├── domain
│   │   ├── SubDomainBrute.py
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   └── dict
│   ├── domainviews.py
│   ├── ipviews.py
│   ├── plugins
│   │   ├── __init__.py
│   │   ├── __pycache__
│   │   ├── hostnamebased
│   │   └── ipbased
│   ├── pluginviews.py
│   ├── scan
│   │   └── __init__.py
│   ├── tasks.py
│   └── utils
│       ├── __init__.py
│       ├── __pycache__
│       └── utils.py
```

- celery_app 目录包含了所有应用代码
- celery_app下domain 用来做子域名爆破的实际代码
- celery_app下plugins 存储了所有的漏洞扫描插件
- celery_app下的tasks.py 是所有的celery任务
- celery_app下(.*)views.py 是用来调度celery任务的代码
- celery_app下utils目录是一些常用工具函数







