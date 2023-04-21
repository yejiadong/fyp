# Generated by Django 3.2 on 2023-04-01 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0028_auto_20230331_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='claim',
            name='is_paraphrased',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='ClaimParaphrases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_content', models.CharField(max_length=500)),
                ('claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='paraphrases', to='database.claim')),
            ],
        ),
    ]