# Generated by Django 4.0.4 on 2022-05-31 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_user_bank_verification_number_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank_verification_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='national_identification_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
