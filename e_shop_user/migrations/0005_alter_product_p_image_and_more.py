# Generated by Django 4.2.7 on 2023-12-05 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop_user', '0004_productimagegallery'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='p_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/products'),
        ),
        migrations.AlterField(
            model_name='productimagegallery',
            name='image',
            field=models.ImageField(upload_to='product-galleries'),
        ),
    ]
