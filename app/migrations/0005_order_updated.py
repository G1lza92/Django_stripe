# Generated by Django 3.2.14 on 2023-02-26 09:42

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_rename_stripe_payment_intent_order_stripe_session_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='updated',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
