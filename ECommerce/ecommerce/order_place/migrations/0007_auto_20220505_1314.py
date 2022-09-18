# Generated by Django 3.2 on 2022-05-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_place', '0006_order_total_product'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdetails',
            name='total_amount',
        ),
        migrations.AddField(
            model_name='order',
            name='total_amount',
            field=models.FloatField(default=0, null=True, verbose_name='Total Amount'),
        ),
        migrations.AlterField(
            model_name='orderdetails',
            name='sub_total',
            field=models.FloatField(default=0, null=True, verbose_name='Sub Total'),
        ),
    ]