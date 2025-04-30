import multiprocessing

bind = '127.0.0.1:8200'
workers = multiprocessing.cpu_count() * 2 + 1 # 进程数量
threads = 10
accesslog = "/var/log/pythonbbs/access.log"
errorlog = "/var/log/pythonbbs/error.log"
preload_app = True
daemon=True