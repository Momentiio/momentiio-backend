# Generated by Django 2.2.8 on 2019-12-31 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20191231_0005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='is_hidden',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='is_private',
        ),
        migrations.AddField(
            model_name='usermodel',
            name='is_private',
            field=models.BooleanField(default=False),
        ),
    ]
