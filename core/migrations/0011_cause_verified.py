# Generated by Django 4.0.1 on 2022-04-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_merge_0008_giveaway_0009_remove_cause_website_uri'),
    ]

    operations = [
        migrations.AddField(
            model_name='cause',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
