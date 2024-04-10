# Generated by Django 3.2.16 on 2024-04-10 16:41

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0002_auto_20240410_1641'),
    ]

    operations = [
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_type', models.CharField(choices=[('full', 'Full'), ('student', 'Students'), ('discount', 'Discount')], max_length=10, verbose_name='Тарифный план')),
                ('discount_percent', models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)], verbose_name='Процент скидки')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Название сервиса')),
                ('full_price', models.PositiveIntegerField(verbose_name='Стоимость')),
            ],
        ),
        migrations.CreateModel(
            name='Subscribtion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='clients.client', verbose_name='Подписчик')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='services.plan', verbose_name='Сервис')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='services.service', verbose_name='Сервис')),
            ],
        ),
    ]