# Generated by Django 3.0.7 on 2022-03-29 09:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectassets',
            name='project_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='projectassets',
            name='severity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectassets',
            name='type',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectips',
            name='project_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='projectvuls',
            name='project_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='projectvuls',
            name='severity',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='projectvuls',
            name='vultype_id',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='iphone',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='level',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='user_id',
            field=models.IntegerField(),
        ),
    ]