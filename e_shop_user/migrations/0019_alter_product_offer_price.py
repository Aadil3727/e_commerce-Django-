# Generated by Django 4.2.7 on 2023-12-06 10:00

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_shop_user', '0018_alter_product_offer_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='offer_price',
            field=models.DecimalField(blank=True, decimal_places=2, default=Decimal('0'), max_digits=10, null=True),
        ),
    ]
