# Generated by Django 2.2.8 on 2020-01-07 06:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invites', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='token',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
