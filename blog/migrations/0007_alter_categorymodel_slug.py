# Generated by Django 4.2 on 2023-05-13 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_categorymodel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorymodel',
            name='slug',
            field=models.SlugField(unique=True),
        ),
    ]
