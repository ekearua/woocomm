# Generated by Django 3.2.8 on 2021-10-26 07:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('order_id', models.PositiveIntegerField(primary_key=True, serialize=False)),
                ('order_first_name', models.CharField(max_length=50)),
                ('order_last_name', models.CharField(max_length=50)),
                ('order_email', models.EmailField(max_length=254)),
                ('order_phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None)),
                ('order_address', models.CharField(max_length=150)),
                ('order_date_created', models.DateTimeField()),
                ('order_payment_confirmation', models.BooleanField(default=True)),
                ('order_date_paid', models.DateTimeField()),
                ('order_amount', models.PositiveIntegerField()),
                ('order_product', models.CharField(max_length=50)),
                ('order_product_quantity', models.PositiveSmallIntegerField()),
                ('order_product_price', models.PositiveSmallIntegerField()),
                ('order_payment_method', models.CharField(max_length=50)),
                ('order_delivery_type', models.CharField(max_length=50)),
                ('order_status', models.CharField(choices=[('processing', 'processing'), ('on-hold', 'on-hold'), ('payment confirmed', 'payment confirmed'), ('order paid', 'order-paid'), ('completed', 'completed'), ('cancelled', 'cancelled'), ('refunded', 'refunded'), ('failed', 'failed'), ('trash', 'trash')], max_length=50)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'order',
                'verbose_name_plural': 'orders',
                'ordering': ['-order_id'],
            },
        ),
    ]
