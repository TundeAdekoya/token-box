# Generated by Django 4.0.4 on 2022-05-22 17:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='transfer',
            name='reference',
            field=models.TextField(blank=True, null=True),
        ),
    ]
