# Generated by Django 3.2 on 2022-05-16 14:22

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0004_auto_20220516_1406'),
    ]

    operations = [
        migrations.AlterField(
            model_name='applicationuser',
            name='country',
            field=django_countries.fields.CountryField(blank=True, default='IN', max_length=2),
        ),
    ]
