# Generated by Django 4.0.4 on 2022-05-15 21:06

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('email', models.EmailField(max_length=300, unique=True)),
                ('phone_number', models.CharField(blank=True, max_length=17, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '+2341234567890'. Up to 17 digits allowed.", regex='^\\+?234?\\d{9,17}$')])),
                ('active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=40)),
                ('last_name', models.CharField(max_length=40)),
                ('date_of_birth', models.DateField(verbose_name='')),
                ('image', models.ImageField(max_length=300, upload_to=None)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('address', models.CharField(max_length=500)),
                ('account_type', models.CharField(choices=[('Select', 'select'), ('Savings', 'savings'), ('Current', 'current')], default='Select', max_length=10)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('national_identification_number', models.IntegerField()),
                ('bank_verification_number', models.IntegerField()),
                ('mothers_maiden_name', models.CharField(max_length=40)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
        ),
        migrations.CreateModel(
            name='ResetPasswordOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('opt_code', models.CharField(max_length=6)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
        migrations.CreateModel(
            name='OTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('otp_code', models.CharField(max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.user')),
            ],
        ),
    ]
