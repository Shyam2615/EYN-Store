# Generated by Django 4.2.7 on 2024-01-06 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0019_alter_checkout_pincode_wishlist'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='size',
            field=models.CharField(default='medium', max_length=100),
        ),
    ]
