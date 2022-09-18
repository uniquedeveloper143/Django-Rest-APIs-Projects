# Generated by Django 3.2 on 2022-05-19 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0010_auto_20220519_0652'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationuser',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='applicationuser',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True),
        ),
    ]
