# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from taskmanagement.celery import app
from spider.extension.facade import WorkerFacade


@app.task
def yjl_task(*args, **kwargs):

    WorkerFacade.process_yjl(kwargs)

@app.task(bind=True, max_retries=5)
def industry_task(self, *args, **kwargs):
    try:
        WorkerFacade.process_industry(kwargs)
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
@app.task
def fund_list_task(*args, **kwargs):
    WorkerFacade.process_fund_list(kwargs)

@app.task(bind=True)
def fund_share_task(*args, **kwargs):
    WorkerFacade.process_share(kwargs)

@app.task
def stock_task(*args, **kwargs):
    WorkerFacade.process_stock(kwargs)

@app.task
def fund_grade_task(*args, **kwargs):
    WorkerFacade.process_fund_grade(kwargs)

@app.task
def fund_return_task(*args, **kwargs):
    WorkerFacade.process_fund_return(kwargs)

@app.task
def stock_grade_task(*args, **kwargs):
    WorkerFacade.process_stock_grade(kwargs)
