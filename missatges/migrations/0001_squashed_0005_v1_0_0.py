# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-10-16 15:36
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('missatges', '0001_initial'), ('missatges', '0002_grupdemissatgeria_motius'), ('missatges', '0003_edited_missatges'), ('missatges', '0004_change_verbose_name'), ('missatges', '0005_add_creada_rename_tancada')]

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversacio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assumpte', models.CharField(max_length=80)),
                ('tancat', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name_plural': 'conversacions',
                'verbose_name': 'conversació',
            },
        ),
        migrations.CreateModel(
            name='EstatMissatge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vist', models.BooleanField(default=False)),
                ('destinatari', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GrupDeMissatgeria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('usuaris', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                ('motius', models.TextField(blank=True, help_text='Motius per enviar missatges a aquest grup. Apareixeràn a "Nou missatge". Un per línia.')),
            ],
            options={
                'verbose_name_plural': 'grups de missatgeria',
            },
        ),
        migrations.CreateModel(
            name='Missatge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordre', models.PositiveSmallIntegerField(editable=False)),
                ('contingut', models.TextField(help_text='Suporta <a href="/markdown">Markdown</a>')),
                ('enviat', models.DateTimeField(auto_now_add=True)),
                ('editat', models.DateTimeField(auto_now=True)),
                ('conversacio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missatges.Conversacio', verbose_name='conversació')),
                ('destinataris', models.ManyToManyField(through='missatges.EstatMissatge', to=settings.AUTH_USER_MODEL)),
                ('per', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ha_enviat', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='estatmissatge',
            name='missatge',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='missatges.Missatge'),
        ),
        migrations.AddField(
            model_name='conversacio',
            name='a',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='missatges.GrupDeMissatgeria'),
        ),
        migrations.AddField(
            model_name='conversacio',
            name='de',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='missatge',
            unique_together=set([('conversacio', 'ordre')]),
        ),
        migrations.AlterModelOptions(
            name='missatge',
            options={'ordering': ['-ordre']},
        ),
        migrations.AddField(
            model_name='missatge',
            name='estat',
            field=models.CharField(blank=True, choices=[('CLOSED', 'Tancat'), ('REOPENED', 'Reobert')], max_length=8),
        ),
        migrations.AlterUniqueTogether(
            name='estatmissatge',
            unique_together=set([('destinatari', 'missatge')]),
        ),
        migrations.AlterField(
            model_name='missatge',
            name='contingut',
            field=models.TextField(blank=True, help_text='Suporta <a href="/markdown">Markdown</a>'),
        ),
        migrations.AlterModelOptions(
            name='estatmissatge',
            options={'verbose_name': 'estat del missatge', 'verbose_name_plural': 'estat dels missatges'},
        ),
        migrations.AlterModelOptions(
            name='conversacio',
            options={'ordering': ['creada', 'tancada'], 'verbose_name': 'conversació', 'verbose_name_plural': 'conversacions'},
        ),
        migrations.RenameField(
            model_name='conversacio',
            old_name='tancat',
            new_name='tancada',
        ),
        migrations.AddField(
            model_name='conversacio',
            name='creada',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]