# Generated by Django 4.2 on 2023-05-17 19:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_productmodel_category'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productmodel',
            name='category',
        ),
        migrations.AddField(
            model_name='productmodel',
            name='category',
            field=models.CharField(blank=True, max_length=12, null=True),
        ),
    ]