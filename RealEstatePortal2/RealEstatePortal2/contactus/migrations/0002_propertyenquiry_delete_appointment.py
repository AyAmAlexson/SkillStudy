# Generated by Django 4.2.4 on 2023-08-12 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contactus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PropertyEnquiry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('client_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=15)),
                ('property_ref', models.CharField(max_length=7, null=True)),
                ('comment', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='Appointment',
        ),
    ]