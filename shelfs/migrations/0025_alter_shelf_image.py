# Generated by Django 5.1.4 on 2025-01-11 15:50

import shelfs.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelfs', '0024_alter_shelf_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shelf',
            name='image',
            field=models.ImageField(default='../static/icons/shelf.svg', upload_to=shelfs.models.shelf_image_upload_path),
        ),
    ]
