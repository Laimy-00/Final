# Generated by Django 4.2.4 on 2023-08-14 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0006_alter_reservation_table'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='table',
            name='is_available',
        ),
        migrations.AlterField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.table'),
        ),
    ]
