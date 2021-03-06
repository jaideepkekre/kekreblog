# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-09 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('name', models.CharField(max_length=30, verbose_name='Default Blog Name')),
                ('time', models.TimeField(auto_now=True)),
                ('content', models.TextField(verbose_name='Empty Blog')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30)),
                ('parent', models.IntegerField()),
                ('time', models.TimeField(auto_now=True)),
                ('content', models.TextField(verbose_name='Null')),
                ('blog_name', models.CharField(max_length=30)),
            ],
        ),
    ]
