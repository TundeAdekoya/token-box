# Generated by Django 4.0.4 on 2022-05-24 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_email_alter_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bank_verification_number',
            field=models.IntegerField(blank=True, max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='national_identification_number',
            field=models.IntegerField(blank=True, max_length=12, null=True),
        ),
    ]
