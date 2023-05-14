# Generated by Django 4.2 on 2023-05-14 17:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0003_alter_portfoliomodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='portfoliomodel',
            name='link_on_project',
            field=models.URLField(blank=True, default='https//:', max_length=128, null=True, unique=True),
        ),
    ]
