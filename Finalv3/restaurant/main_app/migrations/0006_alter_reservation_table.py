# Generated by Django 4.2.4 on 2023-08-14 13:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_alter_dish_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='table',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='main_app.table'),
        ),
    ]