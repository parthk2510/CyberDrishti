# Generated by Django 5.1.7 on 2025-03-12 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhishingDomain',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(unique=True)),
                ('registration_date', models.DateField(auto_now_add=True)),
                ('registrar', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('PENDING', 'Pending Investigation'), ('BLOCKED', 'Domain Blocked'), ('WHITELISTED', 'Legitimate Domain')], default='PENDING', max_length=20)),
                ('ssl_info', models.JSONField(blank=True, null=True)),
                ('screenshot_path', models.CharField(blank=True, max_length=255)),
                ('threat_score', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='DetectionLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detection_time', models.DateTimeField(auto_now_add=True)),
                ('ai_confidence', models.FloatField()),
                ('action_taken', models.CharField(max_length=100)),
                ('evidence', models.JSONField(blank=True, null=True)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core_backend.phishingdomain')),
            ],
            options={
                'ordering': ['-detection_time'],
            },
        ),
    ]
