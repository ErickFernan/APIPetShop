# Generated by Django 4.2 on 2024-10-22 18:03

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('produtos', '0001_initial'),
        ('usuarios', '0001_initial'),
        ('pet', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('appointment_time', models.TimeField(choices=[('06:00:00', '06:00'), ('06:30:00', '06:30'), ('07:00:00', '07:00'), ('07:30:00', '07:30'), ('08:00:00', '08:00'), ('08:30:00', '08:30'), ('09:00:00', '09:00'), ('09:30:00', '09:30'), ('10:00:00', '10:00'), ('10:30:00', '10:30'), ('11:00:00', '11:00'), ('11:30:00', '11:30'), ('12:00:00', '12:00'), ('12:30:00', '12:30'), ('13:00:00', '13:00'), ('13:30:00', '13:30'), ('14:00:00', '14:00'), ('14:30:00', '14:30'), ('15:00:00', '15:00'), ('15:30:00', '15:30'), ('16:00:00', '16:00'), ('16:30:00', '16:30'), ('17:00:00', '17:00'), ('17:30:00', '17:30'), ('18:00:00', '18:00'), ('18:30:00', '18:30'), ('19:00:00', '19:00'), ('19:30:00', '19:30'), ('20:00:00', '20:00'), ('20:30:00', '20:30'), ('21:00:00', '21:00'), ('21:30:00', '21:30')])),
                ('date', models.DateField()),
                ('func_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='usuarios.user')),
                ('pet_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='pet.pet')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ServiceType',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('execution_time', models.TimeField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('appointment_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='service_types', to='banhotosa.appointment')),
                ('product_used_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='service_types', to='produtos.product')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ProductUsed',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('product_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='used_in_services', to='produtos.product')),
                ('service_type_id', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='products_used', to='banhotosa.servicetype')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]