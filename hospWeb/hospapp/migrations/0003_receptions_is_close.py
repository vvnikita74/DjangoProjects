# Generated by Django 4.1.6 on 2023-02-02 01:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospapp', '0002_doctors_alter_customuser_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='receptions',
            name='is_close',
            field=models.BooleanField(default=False, verbose_name='Закрыт'),
        ),
    ]