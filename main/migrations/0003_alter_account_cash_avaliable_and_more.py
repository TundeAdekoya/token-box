# Generated by Django 4.0.4 on 2022-05-22 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_transfer_reference'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='cash_avaliable',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='account',
            name='token_avaliable',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='transfer',
            name='account_no_transferred',
            field=models.IntegerField(blank=True, max_length=12, null=True),
        ),
    ]