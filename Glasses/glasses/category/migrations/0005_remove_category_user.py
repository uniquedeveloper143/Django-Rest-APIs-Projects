# Generated by Django 3.2 on 2022-05-11 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0004_auto_20220511_1155'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='user',
        ),
    ]