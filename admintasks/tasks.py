# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'keping.chu'

from taskmanagement.celery import app
from spider.extension.facade import WorkerFacade


@app.task
def yjl_task(extra):

    WorkerFacade.process_yjl(extra)


@app.task(bind=True, retry=5)
def industry_task(extra):

    WorkerFacade.process_industry(extra)

@app.task
def fund_list_task(extra):
    WorkerFacade.process_fund_list(extra)

@app.task(bind=True)
def fund_share_task(extra):
    WorkerFacade.process_share(extra)

@app.task
def stock_task(extra):
    WorkerFacade.process_stock(extra)

@app.task
def fund_grade_task(extra):
    WorkerFacade.process_fund_grade(extra)

@app.task
def fund_return_task(extra):
    WorkerFacade.process_fund_return(extra)

@app.task
def stock_grade_task(extra):
    WorkerFacade.process_stock_grade(extra)
