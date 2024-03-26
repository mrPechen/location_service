# Generated by Django 4.2.2 on 2024-03-25 11:43

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField()),
                ('state_name', models.CharField()),
                ('zip', models.PositiveIntegerField()),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
            ],
            options={
                'verbose_name': 'Location',
                'verbose_name_plural': 'Locations',
                'db_table': 'location',
            },
        ),
        migrations.CreateModel(
            name='Cargo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1000)])),
                ('description', models.TextField()),
                ('delivery_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='delivery_location', to='api.location')),
                ('pick_up_location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='pick_up_location', to='api.location')),
            ],
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(unique=True)),
                ('capacity', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1000)])),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_location', to='api.location')),
            ],
            options={
                'verbose_name': 'Car',
                'verbose_name_plural': 'Cars',
                'db_table': 'car',
            },
        ),
    ]
