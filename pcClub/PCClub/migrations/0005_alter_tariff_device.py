# Generated by Django 4.1.5 on 2023-01-18 17:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PCClub', '0004_alter_tariff_device'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tariff',
            name='device',
            field=models.CharField(choices=[('P', 'C'), ('PC', 'Console')], default='P', max_length=2, verbose_name='Тип устройства'),
        ),
    ]
