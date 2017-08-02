# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 20:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0023_auto_20170802_0041'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='age',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='usermodel',
            name='name',
            field=models.CharField(max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='email',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='password',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='username',
            field=models.CharField(max_length=30, unique='True'),
        ),
    ]