# Generated by Django 4.2.4 on 2023-08-16 13:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0009_alter_reservation_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='card_number',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
