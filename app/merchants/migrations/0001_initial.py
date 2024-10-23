# Generated by Django 5.1.2 on 2024-10-23 12:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Merchant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('soon', 'Soon'), ('inactive', 'Inactive')], default='inactive', max_length=10)),
                ('name_uz', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('image', models.ImageField(blank=True, null=True, upload_to='images/merchants/')),
            ],
            options={
                'verbose_name': 'Merchant',
                'verbose_name_plural': 'Merchants',
            },
        ),
        migrations.CreateModel(
            name='MerchantCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('active', 'Active'), ('soon', 'Soon'), ('inactive', 'Inactive')], default='inactive', max_length=10)),
                ('name_uz', models.CharField(max_length=255)),
                ('name_en', models.CharField(max_length=255)),
                ('name_ru', models.CharField(max_length=255)),
                ('icon', models.JSONField(default=dict)),
            ],
            options={
                'verbose_name': 'Merchant Category',
                'verbose_name_plural': 'Merchant Categories',
            },
        ),
        migrations.CreateModel(
            name='MerchantField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('value', models.CharField(max_length=255)),
                ('required', models.BooleanField(default=False)),
                ('merchant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fields', to='merchants.merchant')),
            ],
            options={
                'verbose_name': 'Merchant',
                'verbose_name_plural': 'Merchants',
                'indexes': [models.Index(fields=['merchant'], name='merchants_m_merchan_7b6390_idx')],
                'unique_together': {('merchant', 'name')},
            },
        ),
    ]
