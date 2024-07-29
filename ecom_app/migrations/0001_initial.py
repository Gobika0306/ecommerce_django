# Generated by Django 5.0.7 on 2024-07-12 06:44

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('password', models.CharField(max_length=128)),
                ('email_id', models.EmailField(max_length=254, unique=True)),
                ('phone_no', models.CharField(max_length=15)),
                ('address', models.CharField(max_length=250)),
            ],
        ),
    ]
