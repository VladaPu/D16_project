# Generated by Django 4.2.9 on 2024-01-06 09:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mainapp', '0004_alter_posts_author_alter_posts_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='responses',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор отклика'),
        ),
    ]
