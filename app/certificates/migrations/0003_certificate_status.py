# Generated by Django 3.1.7 on 2021-03-01 00:30

import app.certificates.types
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certificates', '0002_auto_20210301_0025'),
    ]

    operations = [
        migrations.AddField(
            model_name='certificate',
            name='status',
            field=models.CharField(choices=[('disabled', 'DISABLED'), ('active', 'ACTIVE')], default=app.certificates.types.CertificateStatuses['ACTIVE'], max_length=255, verbose_name='status'),
        ),
    ]
