# Generated by Django 3.2 on 2022-05-18 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_passwordresetid'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='applicationuser',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=10, max_digits=20, null=True),
        ),
    ]
