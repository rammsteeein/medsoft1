from celery import Celery

celery_app = Celery(
    'tasks',
    broker='memory://',
    backend='rpc://'
)

celery_app.conf.update(
    result_expires=3600,
)