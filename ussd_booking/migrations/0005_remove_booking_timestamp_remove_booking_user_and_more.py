# Generated by Django 4.2.1 on 2023-05-27 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ussd_booking', '0004_complaint_bus_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='booking',
            name='user',
        ),
        migrations.AddField(
            model_name='booking',
            name='date',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='trip',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ussd_booking.trip'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='user_phone',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='booking',
            name='seat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ussd_booking.seat'),
        ),
    ]
