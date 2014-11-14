# !/usr/bin/python
# vim: set fileencoding=utf8 :
#

from django.db import models

# Create your models here.

class Industry(models.Model):
    """
    industry
    """
    name = models.CharField(verbose_name=u'名称', max_length=20)
    code = models.CharField(verbose_name=u'代码', max_length=20)

    class Meta:
        verbose_name = u'行业'


class Stock(models.Model):
    """
    Stock
    """
    name = models.CharField(verbose_name=u'股票名称', max_length=20)
    code = models.CharField(verbose_name=u'股票代码', max_length=20)
    industry = models.ForeignKey(Industry, verbose_name=u'所属行业', null=True)

    class Meta:
        verbose_name = u'股票'





class Fund(models.Model):
    """
    fund
    """
    name = models.CharField(verbose_name=u'基金名称', max_length=20)
    code = models.CharField(verbose_name=u'基金代码', max_length=20, unique=True)
    stocks = models.ManyToManyField(Stock, through='Share', verbose_name=u'持仓', null=True)
    kind = models.CharField(verbose_name=u'类别', max_length=20)

    class Meta:
        verbose_name = u'基金'



class Share(models.Model):
    """
    trade share
    """
    stock = models.ForeignKey(Stock, verbose_name=u'股票')
    fund = models.ForeignKey(Fund, verbose_name=u'基金')
    share = models.FloatField(verbose_name=u'份额')
    amount = models.FloatField(verbose_name=u'金额')

    class Meta:
        verbose_name = u'持有份额'
        unique_together = ('stock', 'fund')


class FundGrade(models.Model):
    """
    grade of fund
    """
    institution = models.CharField(verbose_name=u'评级机构', max_length=20)
    fund = models.ForeignKey(Fund, verbose_name=u'基金')
    star = models.IntegerField(verbose_name=u'级别')


class MoneyFlow(models.Model):
    """
    money flow
    """
    industry = models.ForeignKey(Industry, verbose_name=u'行业')
    director = models.BooleanField(verbose_name=u'流入', default=False)
    amount = models.FloatField(verbose_name=u'金额')
    change_date = models.DateField(verbose_name=u'变化日期', auto_now_add=True)

    class Meta:
        verbose_name = u'资金流向'


class FundJournal(models.Model):
    """
    """
    fund = models.ForeignKey(Fund, verbose_name=u'基金')
    price = models.FloatField(verbose_name=u'市值')
    change_date = models.DateField(verbose_name=u'变化日期', auto_now_add=True)

    class Meta:
        verbose_name = u'基金市值'