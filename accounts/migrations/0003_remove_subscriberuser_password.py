# Generated by Django 3.0.14 on 2023-03-22 12:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_subscriberuser'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='subscriberuser',
            name='password',
        ),
    ]
