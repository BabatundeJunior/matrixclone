# Generated by Django 5.1.2 on 2024-11-12 02:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_feature_instructorcourse_platformcourse_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='duration_days',
            field=models.PositiveIntegerField(blank=True, help_text='Duration of the plan in days'),
        ),
    ]