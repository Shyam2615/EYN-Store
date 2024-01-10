# Generated by Django 4.2.7 on 2023-12-28 09:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('product_uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('updated_at', models.DateField(auto_now_add=True)),
                ('product_category', models.CharField(max_length=100)),
                ('product_image', models.ImageField(upload_to='products')),
                ('product_name', models.CharField(max_length=100)),
                ('real_price', models.IntegerField(default=1)),
                ('discounted_price', models.IntegerField(default=1)),
                ('product_description', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]