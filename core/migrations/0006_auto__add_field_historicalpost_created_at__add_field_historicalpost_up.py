# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'HistoricalPost.created_at'
        db.add_column(u'core_historicalpost', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'HistoricalPost.updated_at'
        db.add_column(u'core_historicalpost', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'HistoricalPost.changed_by_id'
        db.add_column(u'core_historicalpost', u'changed_by_id',
                      self.gf('django.db.models.fields.IntegerField')(db_index=True, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Person.created_at'
        db.add_column(u'core_person', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Person.updated_at'
        db.add_column(u'core_person', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Person.changed_by'
        db.add_column(u'core_person', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_person_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Pledge.created_at'
        db.add_column(u'core_pledge', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Pledge.updated_at'
        db.add_column(u'core_pledge', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Pledge.changed_by'
        db.add_column(u'core_pledge', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_pledge_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Payout.created_at'
        db.add_column(u'core_payout', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Payout.updated_at'
        db.add_column(u'core_payout', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Payout.changed_by'
        db.add_column(u'core_payout', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_payout_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Contribution.created_at'
        db.add_column(u'core_contribution', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Contribution.updated_at'
        db.add_column(u'core_contribution', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Contribution.changed_by'
        db.add_column(u'core_contribution', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_contribution_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Badge.created_at'
        db.add_column(u'core_badge', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Badge.updated_at'
        db.add_column(u'core_badge', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Badge.changed_by'
        db.add_column(u'core_badge', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_badge_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Service.created_at'
        db.add_column(u'core_service', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Service.updated_at'
        db.add_column(u'core_service', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Service.changed_by'
        db.add_column(u'core_service', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_service_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Post.created_at'
        db.add_column(u'core_post', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Post.updated_at'
        db.add_column(u'core_post', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Post.changed_by'
        db.add_column(u'core_post', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_post_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Membership.created_at'
        db.add_column(u'core_membership', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Membership.updated_at'
        db.add_column(u'core_membership', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Membership.changed_by'
        db.add_column(u'core_membership', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_membership_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Project.created_at'
        db.add_column(u'core_project', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.updated_at'
        db.add_column(u'core_project', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Project.changed_by'
        db.add_column(u'core_project', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_project_related', null=True, to=orm['core.Person']),
                      keep_default=False)

        # Adding field 'Media.created_at'
        db.add_column(u'core_media', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Media.updated_at'
        db.add_column(u'core_media', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, default=datetime.datetime(2014, 1, 3, 0, 0), blank=True),
                      keep_default=False)

        # Adding field 'Media.changed_by'
        db.add_column(u'core_media', 'changed_by',
                      self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'core_media_related', null=True, to=orm['core.Person']),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'HistoricalPost.created_at'
        db.delete_column(u'core_historicalpost', 'created_at')

        # Deleting field 'HistoricalPost.updated_at'
        db.delete_column(u'core_historicalpost', 'updated_at')

        # Deleting field 'HistoricalPost.changed_by_id'
        db.delete_column(u'core_historicalpost', u'changed_by_id')

        # Deleting field 'Person.created_at'
        db.delete_column(u'core_person', 'created_at')

        # Deleting field 'Person.updated_at'
        db.delete_column(u'core_person', 'updated_at')

        # Deleting field 'Person.changed_by'
        db.delete_column(u'core_person', 'changed_by_id')

        # Deleting field 'Pledge.created_at'
        db.delete_column(u'core_pledge', 'created_at')

        # Deleting field 'Pledge.updated_at'
        db.delete_column(u'core_pledge', 'updated_at')

        # Deleting field 'Pledge.changed_by'
        db.delete_column(u'core_pledge', 'changed_by_id')

        # Deleting field 'Payout.created_at'
        db.delete_column(u'core_payout', 'created_at')

        # Deleting field 'Payout.updated_at'
        db.delete_column(u'core_payout', 'updated_at')

        # Deleting field 'Payout.changed_by'
        db.delete_column(u'core_payout', 'changed_by_id')

        # Deleting field 'Contribution.created_at'
        db.delete_column(u'core_contribution', 'created_at')

        # Deleting field 'Contribution.updated_at'
        db.delete_column(u'core_contribution', 'updated_at')

        # Deleting field 'Contribution.changed_by'
        db.delete_column(u'core_contribution', 'changed_by_id')

        # Deleting field 'Badge.created_at'
        db.delete_column(u'core_badge', 'created_at')

        # Deleting field 'Badge.updated_at'
        db.delete_column(u'core_badge', 'updated_at')

        # Deleting field 'Badge.changed_by'
        db.delete_column(u'core_badge', 'changed_by_id')

        # Deleting field 'Service.created_at'
        db.delete_column(u'core_service', 'created_at')

        # Deleting field 'Service.updated_at'
        db.delete_column(u'core_service', 'updated_at')

        # Deleting field 'Service.changed_by'
        db.delete_column(u'core_service', 'changed_by_id')

        # Deleting field 'Post.created_at'
        db.delete_column(u'core_post', 'created_at')

        # Deleting field 'Post.updated_at'
        db.delete_column(u'core_post', 'updated_at')

        # Deleting field 'Post.changed_by'
        db.delete_column(u'core_post', 'changed_by_id')

        # Deleting field 'Membership.created_at'
        db.delete_column(u'core_membership', 'created_at')

        # Deleting field 'Membership.updated_at'
        db.delete_column(u'core_membership', 'updated_at')

        # Deleting field 'Membership.changed_by'
        db.delete_column(u'core_membership', 'changed_by_id')

        # Deleting field 'Project.created_at'
        db.delete_column(u'core_project', 'created_at')

        # Deleting field 'Project.updated_at'
        db.delete_column(u'core_project', 'updated_at')

        # Deleting field 'Project.changed_by'
        db.delete_column(u'core_project', 'changed_by_id')

        # Deleting field 'Media.created_at'
        db.delete_column(u'core_media', 'created_at')

        # Deleting field 'Media.updated_at'
        db.delete_column(u'core_media', 'updated_at')

        # Deleting field 'Media.changed_by'
        db.delete_column(u'core_media', 'changed_by_id')


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
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_badge_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.contribution': {
            'Meta': {'object_name': 'Contribution'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_contribution_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'pledge': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Pledge']", 'symmetrical': 'False'}),
            'project': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Project']", 'symmetrical': 'False'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
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
        u'core.media': {
            'Meta': {'object_name': 'Media'},
            'brief': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_media_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'internal_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'original_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.membership': {
            'Meta': {'object_name': 'Membership'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_membership_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'post': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Post']"}),
            'role': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.payout': {
            'Meta': {'object_name': 'Payout'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_payout_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']", 'null': 'True', 'blank': 'True'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']", 'null': 'True', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.person': {
            'Meta': {'object_name': 'Person'},
            'badges': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': u"orm['core.Badge']", 'null': 'True', 'blank': 'True'}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_person_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'core.pledge': {
            'Meta': {'object_name': 'Pledge'},
            'ammount': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'ammount_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_pledge_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'person': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Person']"}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Project']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.post': {
            'Meta': {'object_name': 'Post'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_post_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
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
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_project_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'duration': ('django.db.models.fields.CharField', [], {'default': "'1'", 'max_length': '3'}),
            'frequency': ('django.db.models.fields.CharField', [], {'default': "'WEE'", 'max_length': '3'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TXT'", 'max_length': '3'}),
            'members': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.service': {
            'Meta': {'object_name': 'Service'},
            'changed_by': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'core_service_related'", 'null': 'True', 'to': u"orm['core.Person']"}),
            'cost_per_hour': ('djmoney.models.fields.MoneyField', [], {'max_digits': '10', 'decimal_places': '2', 'default_currency': "'USD'"}),
            'cost_per_hour_currency': ('djmoney.models.fields.CurrencyField', [], {'default': "'USD'"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'prividing_Person': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Person']", 'symmetrical': 'False'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['core']