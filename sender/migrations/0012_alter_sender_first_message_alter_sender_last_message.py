# Generated by Django 4.2 on 2024-09-08 11:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sender', '0011_remove_deliveryattempt_attempt_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sender',
            name='first_message',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 8, 11, 41, 7, 399818, tzinfo=datetime.timezone.utc), verbose_name='дата и время первого письма'),
        ),
        migrations.AlterField(
            model_name='sender',
            name='last_message',
            field=models.DateTimeField(default=datetime.datetime(2024, 9, 8, 11, 41, 7, 399818, tzinfo=datetime.timezone.utc), verbose_name='дата и время последнего письма'),
        ),
    ]
