# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Payout.person'
        db.add_column(u'core_payout', 'person',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Person'], null=True, blank=True),
                      keep_default=False)

        # Adding field 'Payout.project'
        db.add_column(u'core_payout', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Project'], null=True, blank=True),
                      keep_default=False)

        # Removing M2M table for field project on 'Payout'
        db.delete_table(db.shorten_name(u'core_payout_project'))

        # Removing M2M table for field person on 'Payout'
        db.delete_table(db.shorten_name(u'core_payout_person'))

        # Adding field 'Post.project'
        db.add_column(u'core_post', 'project',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['core.Project']),
                      keep_default=False)

        # Adding M2M table for field media on 'Post'
        m2m_table_name = db.shorten_name(u'core_post_media')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('post', models.ForeignKey(orm[u'core.post'], null=False)),
            ('media', models.ForeignKey(orm[u'core.media'], null=False))
        ))
        db.create_unique(m2m_table_name, ['post_id', 'media_id'])


    def backwards(self, orm):
        # Deleting field 'Payout.person'
        db.delete_column(u'core_payout', 'person_id')

        # Deleting field 'Payout.project'
        db.delete_column(u'core_payout', 'project_id')

        # Adding M2M table for field project on 'Payout'
        m2m_table_name = db.shorten_name(u'core_payout_project')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payout', models.ForeignKey(orm[u'core.payout'], null=False)),
            ('project', models.ForeignKey(orm[u'core.project'], null=False))
        ))
        db.create_unique(m2m_table_name, ['payout_id', 'project_id'])

        # Adding M2M table for field person on 'Payout'
        m2m_table_name = db.shorten_name(u'core_payout_person')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('payout', models.ForeignKey(orm[u'core.payout'], null=False)),
            ('person', models.ForeignKey(orm[u'core.person'], null=False))
        ))
        db.create_unique(m2m_table_name, ['payout_id', 'person_id'])

        # Deleting field 'Post.project'
        db.delete_column(u'core_post', 'project_id')

        # Removing M2M table for field media on 'Post'
        db.delete_table(db.shorten_name(u'core_post_media'))


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
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True', 'blank': 'True'})
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
            'media': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Media']", 'symmetrical': 'False'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'through': u"orm['core.Membership']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
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