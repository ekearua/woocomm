# Generated by Django 3.2.8 on 2021-10-25 07:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dash', '0002_auto_20211025_0823'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='order_edited_by',
        ),
        migrations.AddField(
            model_name='orders',
            name='user',
            field=models.ForeignKey(default='User', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
