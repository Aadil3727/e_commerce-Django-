# Generated by Django 4.2.7 on 2023-12-11 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop_admin', '0012_auth_user_forget_password_token_delete_profile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='auth_user',
            name='expire_token',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
