# Generated by Django 4.1.5 on 2023-01-18 16:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCClub', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tariff',
            name='device',
            field=models.CharField(choices=[('P', 'PC'), ('C', 'Console')], default='PC', max_length=2, verbose_name='Тип устройства'),
        ),
        migrations.AlterField(
            model_name='tariff',
            name='cost',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(50)], verbose_name='Стоимость за час'),
        ),
    ]