# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'HistoricalPost'
        db.create_table(u'core_historicalpost', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            (u'project_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalPost'])

        # Adding model 'HistoricalContribution'
        db.create_table(u'core_historicalcontribution', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalContribution'])

        # Adding model 'Pledge'
        db.create_table(u'core_pledge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_pledge_related', null=True, to=orm['auth.User'])),
            ('pledger', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'core', ['Pledge'])

        # Adding model 'Payout'
        db.create_table(u'core_payout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_payout_related', null=True, to=orm['auth.User'])),
            ('payee', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True, blank=True)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'], null=True, blank=True)),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Payout'])

        # Adding model 'Contribution'
        db.create_table(u'core_contribution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_contribution_related', null=True, to=orm['auth.User'])),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Contribution'])

        # Adding M2M table for field contributer on 'Contribution'
        m2m_table_name = db.shorten_name(u'core_contribution_contributer')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contribution', models.ForeignKey(orm[u'core.contribution'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contribution_id', 'user_id'])

        # Adding M2M table for field pledge on 'Contribution'
        m2m_table_name = db.shorten_name(u'core_contribution_pledge')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contribution', models.ForeignKey(orm[u'core.contribution'], null=False)),
            ('pledge', models.ForeignKey(orm[u'core.pledge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contribution_id', 'pledge_id'])

        # Adding M2M table for field project on 'Contribution'
        m2m_table_name = db.shorten_name(u'core_contribution_project')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contribution', models.ForeignKey(orm[u'core.contribution'], null=False)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contribution_id', 'project_id'])

        # Adding model 'Badge'
        db.create_table(u'core_badge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_badge_related', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'core', ['Badge'])

        # Adding model 'Service'
        db.create_table(u'core_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_service_related', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('cost_per_hour_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('cost_per_hour', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding M2M table for field provider on 'Service'
        m2m_table_name = db.shorten_name(u'core_service_provider')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm[u'core.service'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['service_id', 'user_id'])

        # Adding model 'HistoricalPayout'
        db.create_table(u'core_historicalpayout', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            (u'payee_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            (u'project_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalPayout'])

        # Adding model 'Membership'
        db.create_table(u'core_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_membership_related', null=True, to=orm['auth.User'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Post'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Membership'])

        # Adding model 'HistoricalMedia'
        db.create_table(u'core_historicalmedia', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('original_file', self.gf('django.db.models.fields.TextField')(max_length=100)),
            ('internal_file', self.gf('django.db.models.fields.TextField')(max_length=100, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('brief', self.gf('django.db.models.fields.TextField')(default='')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalMedia'])

        # Adding model 'HistoricalService'
        db.create_table(u'core_historicalservice', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('cost_per_hour_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('cost_per_hour', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalService'])

        # Adding model 'Post'
        db.create_table(u'core_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_post_related', null=True, to=orm['auth.User'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'core', ['Post'])

        # Adding M2M table for field media on 'Post'
        m2m_table_name = db.shorten_name(u'core_post_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'core.post'], null=False)),
            ('media', models.ForeignKey(orm[u'core.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'media_id'])

        # Adding model 'HistoricalProject'
        db.create_table(u'core_historicalproject', (
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            (u'changed_by_id', self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('brief', self.gf('django.db.models.fields.TextField')(default='')),
            ('medium', self.gf('django.db.models.fields.CharField')(default='TXT', max_length=3)),
            ('duration', self.gf('django.db.models.fields.CharField')(default='1', max_length=3)),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='WEE', max_length=3)),
            ('ask_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ask', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            (u'history_id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            (u'history_date', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            (u'history_user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'], null=True)),
            (u'history_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal(u'core', ['HistoricalProject'])

        # Adding model 'Project'
        db.create_table(u'core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_project_related', null=True, to=orm['auth.User'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('brief', self.gf('django.db.models.fields.TextField')(default='')),
            ('medium', self.gf('django.db.models.fields.CharField')(default='TXT', max_length=3)),
            ('duration', self.gf('django.db.models.fields.CharField')(default='1', max_length=3)),
            ('frequency', self.gf('django.db.models.fields.CharField')(default='WEE', max_length=3)),
            ('ask_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ask', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Project'])

        # Adding M2M table for field members on 'Project'
        m2m_table_name = db.shorten_name(u'core_project_members')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'user_id'])

        # Adding model 'Media'
        db.create_table(u'core_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('changed_by', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_media_related', null=True, to=orm['auth.User'])),
            ('original_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('internal_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('brief', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal(u'core', ['Media'])


    def backwards(self, orm):
        # Deleting model 'HistoricalPost'
        db.delete_table(u'core_historicalpost')

        # Deleting model 'HistoricalContribution'
        db.delete_table(u'core_historicalcontribution')

        # Deleting model 'Pledge'
        db.delete_table(u'core_pledge')

        # Deleting model 'Payout'
        db.delete_table(u'core_payout')

        # Deleting model 'Contribution'
        db.delete_table(u'core_contribution')

        # Removing M2M table for field contributer on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_contributer'))

        # Removing M2M table for field pledge on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_pledge'))

        # Removing M2M table for field project on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_project'))

        # Deleting model 'Badge'
        db.delete_table(u'core_badge')

        # Deleting model 'Service'
        db.delete_table(u'core_service')

        # Removing M2M table for field provider on 'Service'
        db.delete_table(db.shorten_name(u'core_service_provider'))

        # Deleting model 'HistoricalPayout'
        db.delete_table(u'core_historicalpayout')

        # Deleting model 'Membership'
        db.delete_table(u'core_membership')

        # Deleting model 'HistoricalMedia'
        db.delete_table(u'core_historicalmedia')

        # Deleting model 'HistoricalService'
        db.delete_table(u'core_historicalservice')

        # Deleting model 'Post'
        db.delete_table(u'core_post')

        # Removing M2M table for field media on 'Post'
        db.delete_table(db.shorten_name(u'core_post_media'))

        # Deleting model 'HistoricalProject'
        db.delete_table(u'core_historicalproject')

        # Deleting model 'Project'
        db.delete_table(u'core_project')

        # Removing M2M table for field members on 'Project'
        db.delete_table(db.shorten_name(u'core_project_members'))

        # Deleting model 'Media'
        db.delete_table(u'core_media')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.badge': {
            'Meta': {'object_name': 'Badge'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_badge_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.contribution': {
            'Meta': {'object_name': 'Contribution'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_contribution_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'contributer': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pledge': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Pledge']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Project']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.historicalcontribution': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalContribution'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.historicalmedia': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalMedia'},
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'internal_file': ('django.db.models.fields.TextField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.TextField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.historicalpayout': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalPayout'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            u'payee_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            u'project_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.historicalpost': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalPost'},
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            u'project_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.historicalproject': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalProject'},
            'ask': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ask_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'WEE'", 'max_length': '3'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.historicalservice': {
            'Meta': {'ordering': "(u'-history_date', u'-history_id')", 'object_name': 'HistoricalService'},
            u'changed_by_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'cost_per_hour': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'cost_per_hour_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            u'history_date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'history_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'history_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            u'history_user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'})
        },
        u'core.media': {
            'Meta': {'object_name': 'Media'},
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_media_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.membership': {
            'Meta': {'object_name': 'Membership'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_membership_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Post']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'core.payout': {
            'Meta': {'object_name': 'Payout'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_payout_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'payee': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_pledge_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pledger': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.post': {
            'Meta': {'object_name': 'Post'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_post_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Media']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'ask': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ask_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_project_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'WEE'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_service_related'", 'null': 'True', 'to': u"orm['auth.User']"}),
            'cost_per_hour': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'cost_per_hour_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'provider': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.User']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']