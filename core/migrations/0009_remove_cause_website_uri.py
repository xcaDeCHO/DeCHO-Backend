# Generated by Django 4.0.1 on 2022-03-10 11:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_cause_website_uri'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cause',
            name='website_uri',
        ),
    ]