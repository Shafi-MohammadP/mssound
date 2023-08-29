# Generated by Django 4.2.1 on 2023-07-12 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50, unique=True)),
                ('product_price', models.IntegerField()),
                ('product_image', models.ImageField(default='No image available', upload_to='photos/product')),
                ('slug', models.SlugField(max_length=250, unique=True)),
            ],
        ),
    ]
