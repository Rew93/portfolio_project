# Generated by Django 4.2 on 2023-04-22 21:14

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog', '0003_alter_blogmodel_author_alter_commentsmodel_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentsmodel',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]