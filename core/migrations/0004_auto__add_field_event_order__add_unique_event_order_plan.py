# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.order'
        db.add_column('table_event', 'order',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)

        # Adding unique constraint on 'Event', fields ['order', 'plan']
        db.create_unique('table_event', ['order', 'plan_id'])


    def backwards(self, orm):
        # Removing unique constraint on 'Event', fields ['order', 'plan']
        db.delete_unique('table_event', ['order', 'plan_id'])

        # Deleting field 'Event.order'
        db.delete_column('table_event', 'order')


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
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.collaboration': {
            'Meta': {'unique_together': "(('collaborator', 'plan'),)", 'object_name': 'Collaboration', 'db_table': "'table_collaboration'"},
            'collaborator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collaboration_collaborator'", 'to': u"orm['core.User']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'collaboration_plan'", 'to': u"orm['core.Plan']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.event': {
            'Meta': {'unique_together': "(('order', 'plan'),)", 'object_name': 'Event', 'db_table': "'table_event'"},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'header': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'plan': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Plan']"}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'core.plan': {
            'Meta': {'object_name': 'Plan', 'db_table': "'table_plan'"},
            'collaborator': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.User']", 'through': u"orm['core.Collaboration']", 'symmetrical': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'core.user': {
            'Meta': {'object_name': 'User', 'db_table': "'table_user'"},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '200', 'db_index': 'True'}),
            'facebook_id': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'tz_offset': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        }
    }

    complete_apps = ['core']