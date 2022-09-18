# Generated by Django 3.2 on 2022-05-05 12:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_address'),
        ('order_place', '0002_auto_20220505_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='address',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='custom_auth.address'),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_charge',
            field=models.FloatField(default=10, null=True, verbose_name='Shipping Charge'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('canceled', 'Canceled'), ('returned', 'Returned'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('on_the_way', 'On The Way'), ('dispatch', 'Dispatch'), ('shipped', 'Sipped'), ('delivered', 'Delivered')], default='pending', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_type',
            field=models.CharField(choices=[('cod', 'Cash On Delivery'), ('upi', 'UPI'), ('card', 'Card')], default='cod', max_length=10),
        ),
    ]
