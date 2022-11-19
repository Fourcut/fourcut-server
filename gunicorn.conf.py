port = 8000
bind = f'0.0.0.0:{port}'
workers = 4
accesslog = './log/access_log.txt'
errorlog = './log/error_log.txt'
worker_class = 'uvicorn.workers.UvicornWorker'
