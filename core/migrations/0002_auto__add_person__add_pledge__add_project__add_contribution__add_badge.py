# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Person'
        db.create_table(u'core_person', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
        ))
        db.send_create_signal(u'core', ['Person'])

        # Adding M2M table for field badges on 'Person'
        m2m_table_name = db.shorten_name(u'core_person_badges')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False)),
            ('badge', models.ForeignKey(orm[u'core.badge'], null=False))
        ))
        db.create_unique(m2m_table_name, ['person_id', 'badge_id'])

        # Adding model 'Pledge'
        db.create_table(u'core_pledge', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'])),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
            ('token', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'core', ['Pledge'])

        # Adding model 'Project'
        db.create_table(u'core_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
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
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['project_id', 'person_id'])

        # Adding model 'Contribution'
        db.create_table(u'core_contribution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Contribution'])

        # Adding M2M table for field person on 'Contribution'
        m2m_table_name = db.shorten_name(u'core_contribution_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('contribution', models.ForeignKey(orm[u'core.contribution'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['contribution_id', 'person_id'])

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
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
        ))
        db.send_create_signal(u'core', ['Badge'])

        # Adding model 'Post'
        db.create_table(u'core_post', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=60)),
        ))
        db.send_create_signal(u'core', ['Post'])

        # Adding model 'Service'
        db.create_table(u'core_service', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=300)),
            ('cost_per_hour_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('cost_per_hour', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Service'])

        # Adding M2M table for field prividing_Person on 'Service'
        m2m_table_name = db.shorten_name(u'core_service_prividing_Person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('service', models.ForeignKey(orm[u'core.service'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['service_id', 'person_id'])

        # Adding model 'Membership'
        db.create_table(u'core_membership', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('person', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'])),
            ('post', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Post'])),
            ('role', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Membership'])

        # Adding model 'Payout'
        db.create_table(u'core_payout', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ammount_currency', self.gf('djmoney.models.fields.CurrencyField')(default='USD')),
            ('ammount', self.gf('djmoney.models.fields.MoneyField')(max_digits=10, decimal_places=2, default_currency='USD')),
        ))
        db.send_create_signal(u'core', ['Payout'])

        # Adding M2M table for field person on 'Payout'
        m2m_table_name = db.shorten_name(u'core_payout_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payout', models.ForeignKey(orm[u'core.payout'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['payout_id', 'person_id'])

        # Adding M2M table for field project on 'Payout'
        m2m_table_name = db.shorten_name(u'core_payout_project')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payout', models.ForeignKey(orm[u'core.payout'], null=False)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['payout_id', 'project_id'])

        # Adding model 'Media'
        db.create_table(u'core_media', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('original_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('internal_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('medium', self.gf('django.db.models.fields.CharField')(default='TXT', max_length=3, null=True, blank=True)),
        ))
        db.send_create_signal(u'core', ['Media'])


    def backwards(self, orm):
        # Deleting model 'Person'
        db.delete_table(u'core_person')

        # Removing M2M table for field badges on 'Person'
        db.delete_table(db.shorten_name(u'core_person_badges'))

        # Deleting model 'Pledge'
        db.delete_table(u'core_pledge')

        # Deleting model 'Project'
        db.delete_table(u'core_project')

        # Removing M2M table for field members on 'Project'
        db.delete_table(db.shorten_name(u'core_project_members'))

        # Deleting model 'Contribution'
        db.delete_table(u'core_contribution')

        # Removing M2M table for field person on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_person'))

        # Removing M2M table for field pledge on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_pledge'))

        # Removing M2M table for field project on 'Contribution'
        db.delete_table(db.shorten_name(u'core_contribution_project'))

        # Deleting model 'Badge'
        db.delete_table(u'core_badge')

        # Deleting model 'Post'
        db.delete_table(u'core_post')

        # Deleting model 'Service'
        db.delete_table(u'core_service')

        # Removing M2M table for field prividing_Person on 'Service'
        db.delete_table(db.shorten_name(u'core_service_prividing_Person'))

        # Deleting model 'Membership'
        db.delete_table(u'core_membership')

        # Deleting model 'Payout'
        db.delete_table(u'core_payout')

        # Removing M2M table for field person on 'Payout'
        db.delete_table(db.shorten_name(u'core_payout_person'))

        # Removing M2M table for field project on 'Payout'
        db.delete_table(db.shorten_name(u'core_payout_project'))

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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'core.contribution': {
            'Meta': {'object_name': 'Contribution'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'pledge': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Pledge']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Project']", 'symmetrical': 'False'})
        },
        u'core.media': {
            'Meta': {'object_name': 'Media'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'core.membership': {
            'Meta': {'object_name': 'Membership'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Post']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.payout': {
            'Meta': {'object_name': 'Payout'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Project']", 'symmetrical': 'False'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Badge']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'core.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'core.post': {
            'Meta': {'object_name': 'Post'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'through': u"orm['core.Membership']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        u'core.project': {
            'Meta': {'object_name': 'Project'},
            'ask': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ask_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'WEE'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service'},
            'cost_per_hour': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'cost_per_hour_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prividing_Person': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'})
        }
    }

    complete_apps = ['core']