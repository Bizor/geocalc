# Generated by Django 2.0.1 on 2018-02-06 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('geobase', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pointbase',
            name='point_csid',
        ),
        migrations.RemoveField(
            model_name='pointbase',
            name='point_owner',
        ),
        migrations.RemoveField(
            model_name='pointbase',
            name='point_project',
        ),
        migrations.AddField(
            model_name='project',
            name='project_points',
            field=models.TextField(default='', verbose_name='Каталог точек'),
        ),
        migrations.DeleteModel(
            name='PointBase',
        ),
    ]
