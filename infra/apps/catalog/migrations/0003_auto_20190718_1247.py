# Generated by Django 2.2.2 on 2019-07-18 12:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_auto_20190716_1513'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Catalog',
            new_name='CatalogUpload',
        ),
    ]