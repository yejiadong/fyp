# Generated by Django 3.2 on 2023-03-26 12:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0020_remove_claim_labeller_claim_unique'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evidence',
            name='original_id',
        ),
    ]
