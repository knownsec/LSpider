# Generated by Django 3.0.1 on 2020-04-23 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spider', '0004_auto_20200414_1443'),
    ]

    operations = [
        migrations.AlterField(
            model_name='urltable',
            name='url',
            field=models.CharField(max_length=1500),
        ),
    ]