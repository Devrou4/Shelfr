# Generated by Django 5.1.4 on 2025-02-08 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shelfs', '0004_alter_item_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='title',
            field=models.CharField(max_length=25),
        ),
    ]
