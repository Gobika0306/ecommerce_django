# Generated by Django 5.0.7 on 2024-07-24 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('ecom_app', '0005_remove_customuser_user_type_profile_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='selected_permissions',
            field=models.ManyToManyField(blank=True, to='auth.permission'),
        ),
    ]
