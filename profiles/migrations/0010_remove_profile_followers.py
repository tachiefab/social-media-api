# Generated by Django 3.0 on 2020-06-05 23:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20200605_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='followers',
        ),
    ]
