# Generated by Django 4.2.7 on 2024-01-08 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0020_products_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart_items',
            name='size',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
