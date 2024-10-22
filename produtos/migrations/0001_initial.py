# Generated by Django 4.2 on 2024-10-22 18:03

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50)),
                ('brand', models.CharField(blank=True, max_length=50, null=True)),
                ('sale_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('stock', models.PositiveSmallIntegerField()),
                ('photo_path', models.CharField(blank=True, max_length=100, null=True)),
                ('product_type', models.CharField(choices=[('remedio', 'Remedio'), ('perfumaria', 'Perfumaria'), ('vacina', 'Vacina'), ('vestuario', 'Vestuario'), ('alimento', 'Alimento'), ('outro', 'Outro')], max_length=50)),
                ('storage_location', models.CharField(blank=True, max_length=50, null=True)),
                ('expiration_date', models.DateField()),
                ('purchase_date', models.DateField()),
                ('purchase_price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
