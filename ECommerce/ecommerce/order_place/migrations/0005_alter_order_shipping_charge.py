# Generated by Django 3.2 on 2022-05-05 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_place', '0004_auto_20220505_1228'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='shipping_charge',
            field=models.FloatField(default=0, null=True, verbose_name='Shipping Charge'),
        ),
    ]
