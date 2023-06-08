# Generated by Django 4.2 on 2023-05-17 20:02

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_alter_categoryproductmodel_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productmodel',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]