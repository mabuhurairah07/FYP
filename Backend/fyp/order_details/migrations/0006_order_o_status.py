# Generated by Django 4.2.4 on 2023-08-17 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_details', '0005_auto_20230803_1945'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='o_status',
            field=models.CharField(default='In Process', max_length=200),
        ),
    ]