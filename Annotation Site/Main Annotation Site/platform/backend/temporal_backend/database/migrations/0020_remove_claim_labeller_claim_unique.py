# Generated by Django 3.2 on 2023-03-26 11:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0019_claim_labeller_claim_unique'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='claim',
            name='labeller_claim_unique',
        ),
    ]
