# Generated by Django 2.2.2 on 2019-07-26 17:51

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalog', '0012_auto_20190725_1743'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='admins',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
