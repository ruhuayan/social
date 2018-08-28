# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0002_auto_20170501_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('handle', models.TextField()),
                ('message', models.TextField()),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now, db_index=True)),
            ],
        ),
        migrations.AlterField(
            model_name='socialgroup',
            name='name',
            field=models.CharField(unique=True, max_length=150),
        ),
        migrations.AddField(
            model_name='chat',
            name='sgroup',
            field=models.ForeignKey(related_name='chats', to='membership.SocialGroup'),
        ),
    ]
