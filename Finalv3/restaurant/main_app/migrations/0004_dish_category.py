# Generated by Django 4.2.4 on 2023-08-14 11:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_alter_customuser_position_alter_customuser_schedule'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='category',
            field=models.CharField(choices=[('starter', 'Starter'), ('main', 'Main'), ('side', 'Side'), ('disert', 'Disert'), ('drink', 'Drink')], default='main', max_length=20),
        ),
    ]