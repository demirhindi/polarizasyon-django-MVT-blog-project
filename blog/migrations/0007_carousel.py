# Generated by Django 3.0.14 on 2023-03-28 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_contact_created_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Carousel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=150)),
                ('url', models.CharField(blank=True, max_length=350)),
                ('image', models.ImageField(blank=True, upload_to='carousel/Images')),
            ],
        ),
    ]
