# Generated by Django 3.0.14 on 2023-03-22 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_blogcontext_click_count'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(blank=True, max_length=150)),
                ('subject', models.CharField(blank=True, max_length=300)),
                ('message', models.TextField(blank=True, max_length=10000)),
            ],
            options={
                'ordering': ['-id'],
                'get_latest_by': 'id',
            },
        ),
    ]