# Generated by Django 4.0.4 on 2022-05-31 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_account_bank_name_alter_account_token_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transfer',
            name='account_no_transferred',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
