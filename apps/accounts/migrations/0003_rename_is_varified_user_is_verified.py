# Generated by Django 4.2.3 on 2023-07-21 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_varified',
            new_name='is_verified',
        ),
    ]