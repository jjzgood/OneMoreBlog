# Generated by Django 2.2.3 on 2020-05-05 14:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_auto_20200503_2209'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views',
            field=models.PositiveIntegerField(default=0, editable=False),
        ),
    ]
