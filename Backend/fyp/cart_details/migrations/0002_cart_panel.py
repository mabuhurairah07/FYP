# Generated by Django 4.2.4 on 2023-09-11 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart_details', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='panel',
            field=models.IntegerField(default=1),
        ),
    ]
