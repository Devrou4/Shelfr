# Generated by Django 5.1.4 on 2025-01-09 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelfs', '0006_alter_shelf_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='content',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='shelf',
            name='content',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]
