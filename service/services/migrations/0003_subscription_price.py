# Generated by Django 3.2.16 on 2024-04-11 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0002_rename_subscribtion_subscription'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='price',
            field=models.PositiveIntegerField(default=0, verbose_name='Стоимость'),
        ),
    ]
