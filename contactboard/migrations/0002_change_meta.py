# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 14:39
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contactboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='alumne',
            options={'ordering': ['cognoms', 'nom']},
        ),
        migrations.AlterModelOptions(
            name='classe',
            options={'ordering': ['curs', 'nom']},
        ),
        migrations.AlterModelOptions(
            name='curs',
            options={'ordering': ['ordre', 'nom'], 'verbose_name_plural': 'cursos'},
        ),
    ]
