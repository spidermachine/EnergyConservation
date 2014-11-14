# !/usr/bin/python
# vim: set fileencoding=utf8 :
#
__author__ = 'cping.ju'

from taskmanagement.celery import app
from spider.extension.facade import WorkerFacade


@app.task()
def yjl_task(extra):

    WorkerFacade.process_yjl_worker(extra)


@app.task()
def industry_task(extra):

    WorkerFacade.process_industry_worker(extra)