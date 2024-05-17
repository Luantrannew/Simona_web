# Generated by Django 5.0.6 on 2024-05-15 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('record', '0006_alter_product_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order_From_Customer',
            fields=[
                ('order_code', models.CharField(default=True, max_length=10, primary_key=True, serialize=False)),
                ('time', models.DateTimeField()),
                ('cus_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.customer')),
            ],
        ),
        migrations.CreateModel(
            name='Order_Line',
            fields=[
                ('order_line', models.IntegerField(default=True, primary_key=True, serialize=False)),
                ('SL', models.IntegerField()),
                ('Thanhtien', models.DecimalField(decimal_places=0, max_digits=6)),
                ('order_code', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.order_from_customer')),
                ('product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='record.product')),
            ],
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
