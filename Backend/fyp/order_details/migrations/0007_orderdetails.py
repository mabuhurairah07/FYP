# Generated by Django 4.2.4 on 2023-08-30 15:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_details', '0015_remove_product_sub_category_alter_product_p_status_and_more'),
        ('order_details', '0006_order_o_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('od_id', models.AutoField(primary_key=True, serialize=False)),
                ('actual_price', models.CharField(max_length=200)),
                ('sale_price', models.CharField(max_length=200)),
                ('discount', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField()),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_details.order')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.product')),
                ('variation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_details.variation')),
            ],
        ),
    ]
