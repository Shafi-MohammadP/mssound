# Generated by Django 4.2.3 on 2023-08-03 05:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0005_alter_wishlist_product_qty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wishlist',
            name='product_qty',
        ),
    ]