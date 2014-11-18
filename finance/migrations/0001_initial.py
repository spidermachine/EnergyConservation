# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Industry'
        db.create_table(u'finance_industry', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'finance', ['Industry'])

        # Adding model 'Stock'
        db.create_table(u'finance_stock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Industry'], null=True)),
        ))
        db.send_create_signal(u'finance', ['Stock'])

        # Adding model 'Fund'
        db.create_table(u'finance_fund', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('code', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20)),
            ('kind', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'finance', ['Fund'])

        # Adding model 'Share'
        db.create_table(u'finance_share', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('stock', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Stock'])),
            ('fund', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Fund'])),
            ('share', self.gf('django.db.models.fields.FloatField')()),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
        ))
        db.send_create_signal(u'finance', ['Share'])

        # Adding unique constraint on 'Share', fields ['stock', 'fund']
        db.create_unique(u'finance_share', ['stock_id', 'fund_id'])

        # Adding model 'FundGrade'
        db.create_table(u'finance_fundgrade', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('institution', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('fund', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Fund'])),
            ('star', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'finance', ['FundGrade'])

        # Adding model 'MoneyFlow'
        db.create_table(u'finance_moneyflow', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('industry', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Industry'])),
            ('director', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('amount', self.gf('django.db.models.fields.FloatField')()),
            ('change_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'finance', ['MoneyFlow'])

        # Adding model 'FundJournal'
        db.create_table(u'finance_fundjournal', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('fund', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['finance.Fund'])),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('change_date', self.gf('django.db.models.fields.DateField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'finance', ['FundJournal'])


    def backwards(self, orm):
        # Removing unique constraint on 'Share', fields ['stock', 'fund']
        db.delete_unique(u'finance_share', ['stock_id', 'fund_id'])

        # Deleting model 'Industry'
        db.delete_table(u'finance_industry')

        # Deleting model 'Stock'
        db.delete_table(u'finance_stock')

        # Deleting model 'Fund'
        db.delete_table(u'finance_fund')

        # Deleting model 'Share'
        db.delete_table(u'finance_share')

        # Deleting model 'FundGrade'
        db.delete_table(u'finance_fundgrade')

        # Deleting model 'MoneyFlow'
        db.delete_table(u'finance_moneyflow')

        # Deleting model 'FundJournal'
        db.delete_table(u'finance_fundjournal')


    models = {
        u'finance.fund': {
            'Meta': {'object_name': 'Fund'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kind': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'stocks': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['finance.Stock']", 'null': 'True', 'through': u"orm['finance.Share']", 'symmetrical': 'False'})
        },
        u'finance.fundgrade': {
            'Meta': {'object_name': 'FundGrade'},
            'fund': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Fund']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institution': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'star': ('django.db.models.fields.IntegerField', [], {})
        },
        u'finance.fundjournal': {
            'Meta': {'object_name': 'FundJournal'},
            'change_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fund': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Fund']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        u'finance.industry': {
            'Meta': {'object_name': 'Industry'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'finance.moneyflow': {
            'Meta': {'object_name': 'MoneyFlow'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'change_date': ('django.db.models.fields.DateField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'director': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Industry']"})
        },
        u'finance.share': {
            'Meta': {'unique_together': "(('stock', 'fund'),)", 'object_name': 'Share'},
            'amount': ('django.db.models.fields.FloatField', [], {}),
            'fund': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Fund']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'share': ('django.db.models.fields.FloatField', [], {}),
            'stock': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Stock']"})
        },
        u'finance.stock': {
            'Meta': {'object_name': 'Stock'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'industry': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['finance.Industry']", 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        }
    }

    complete_apps = ['finance']