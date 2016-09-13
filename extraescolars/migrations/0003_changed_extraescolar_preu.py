# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-10 11:33
from __future__ import unicode_literals

from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extraescolars', '0002_update_descriptions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraescolar',
            name='preu',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), help_text='Preu en euros. Ha de ser major o igual a 0 i menor que 100', max_digits=4, validators=[django.core.validators.DecimalValidator(4, 2), django.core.validators.MinValueValidator(0.0)]),
        ),
    ]
