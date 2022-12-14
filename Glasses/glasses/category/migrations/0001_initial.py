# Generated by Django 3.2 on 2022-05-11 08:55

from django.db import migrations, models
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, editable=False, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, editable=False, verbose_name='modified')),
                ('category_name', models.CharField(error_messages={'unique': 'A category with that name is already exists!!'}, max_length=50, unique=True, verbose_name='Category name ')),
                ('slug', models.SlugField(blank=True, max_length=120, null=True, verbose_name='Slug')),
            ],
            options={
                'verbose_name': 'Category',
            },
        ),
    ]
