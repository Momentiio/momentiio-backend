# Generated by Django 2.2.8 on 2020-02-07 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20200123_0437'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageFilter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=25)),
                ('filter', models.CharField(max_length=100, null=True)),
                ('background', models.CharField(max_length=250, null=True)),
                ('opacity', models.CharField(max_length=5, null=True)),
                ('blend_mode', models.CharField(max_length=250, null=True)),
            ],
        ),
    ]