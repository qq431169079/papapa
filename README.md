# papapa
一款用于资产发现和批量poc探测的扫描器

## 搭建方法
- 首先启动redis
 
```
redis-server
```

![](http://tiaogithub.cn-bj.ufileos.com/papapa01.png)
- 启动mongodb

```
 mongod --dbpath
```
![](http://tiaogithub.cn-bj.ufileos.com/papapa02.png)
- 在项目目录下启动celery

```
papapa_venv/bin/celery worker -A run.celery --loglevel=info
``` 
![](http://tiaogithub.cn-bj.ufileos.com/papapa03.png)







