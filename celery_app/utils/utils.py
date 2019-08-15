import time

#获取当前时间
def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
