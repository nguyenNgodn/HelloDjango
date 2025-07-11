# Generated by Django 5.2.3 on 2025-07-09 04:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0002_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='userapp.user')),
            ],
        ),
    ]
