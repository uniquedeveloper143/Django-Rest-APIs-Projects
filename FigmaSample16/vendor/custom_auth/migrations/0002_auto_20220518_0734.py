# Generated by Django 3.2 on 2022-05-18 07:34

from django.db import migrations, models
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='applicationuser',
            name='check_agree',
            field=models.BooleanField(default=False, help_text='Please check term and conditions.', verbose_name='Agree'),
        ),
        migrations.AlterField(
            model_name='applicationuser',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(blank=True, error_messages={'unique': 'A user that phone number already exists.'}, max_length=128, null=True, region=None, unique=True, verbose_name='Phone'),
        ),
    ]
