# Generated by Django 4.2.7 on 2024-01-02 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_cart_cart_items'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='cart',
            new_name='user',
        ),
    ]
