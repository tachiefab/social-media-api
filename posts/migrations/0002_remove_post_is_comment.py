# Generated by Django 3.0 on 2020-06-13 02:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='is_comment',
        ),
    ]
