# -*- coding:utf-8 -*-
import multiprocessing

bind = '127.0.0.1:5000'
backlog = 2048

workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

spew = False

daemon = False
pidfile = None

errorlog = '/root/web_wechat/log/gun_error.log'
loglevel = 'info'
accesslog = '/root/web_wechat/log/gun_access.log'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s'
