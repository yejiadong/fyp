# Generated by Django 3.2 on 2023-03-31 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0027_auto_20230327_1552'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='evidence',
            name='agreement_score',
        ),
        migrations.AddField(
            model_name='evidence',
            name='manual_review',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='TemporalClaimSection',
        ),
    ]
