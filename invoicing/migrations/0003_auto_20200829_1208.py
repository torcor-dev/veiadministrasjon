# Generated by Django 3.0.8 on 2020-08-29 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoicing', '0002_pris_beskjed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pris',
            name='beskjed',
        ),
        migrations.AddField(
            model_name='faktura',
            name='beskjed',
            field=models.TextField(blank=True, null=True),
        ),
    ]
