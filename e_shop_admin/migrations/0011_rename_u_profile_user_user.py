# Generated by Django 4.2.7 on 2023-12-11 07:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop_admin', '0010_rename_user_profile_user_u'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile_user',
            old_name='u',
            new_name='user',
        ),
    ]
