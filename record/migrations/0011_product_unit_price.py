# Generated by Django 5.0.6 on 2024-05-17 03:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0010_rename_order_from_customer_orderfromcustomer_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='unit_price',
            field=models.IntegerField(default=True),
        ),
    ]
