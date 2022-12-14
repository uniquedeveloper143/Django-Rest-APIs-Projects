# Generated by Django 3.2 on 2022-05-05 12:28

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_alter_productphoto_product'),
        ('order_place', '0003_auto_20220505_1205'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.RemoveField(
            model_name='order',
            name='product',
        ),
        migrations.RemoveField(
            model_name='order',
            name='quantity',
        ),
        migrations.CreateModel(
            name='OrderDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('price', models.FloatField(verbose_name='selling price')),
                ('quantity', models.FloatField(verbose_name='Quantity')),
                ('sub_total', models.FloatField(default=10, null=True, verbose_name='Sub Total')),
                ('total_amount', models.FloatField(verbose_name='Total Amount')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_place.order')),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='product.product')),
            ],
            options={
                'verbose_name': 'OrderDetail',
                'verbose_name_plural': 'OrderDetails',
            },
        ),
    ]
