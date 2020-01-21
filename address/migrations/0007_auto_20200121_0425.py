# Generated by Django 2.2.8 on 2020-01-21 04:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('address', '0006_auto_20191229_0912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='stateprovince',
            name='country',
        ),
        migrations.AlterField(
            model_name='address',
            name='country',
            field=django_countries.fields.CountryField(default='US', max_length=2),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_address', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='StateProvince',
        ),
    ]
