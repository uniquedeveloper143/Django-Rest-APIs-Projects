# Generated by Django 3.2 on 2022-05-05 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0003_auto_20220504_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='slug',
            field=models.SlugField(blank=True, max_length=250, null=True, verbose_name='slug'),
        ),
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.PositiveIntegerField(default=1, verbose_name='Quantity'),
        ),
    ]
