# Generated by Django 3.0.14 on 2023-03-28 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0009_auto_20230329_0123'),
    ]

    operations = [
        migrations.AlterField(
            model_name='authorinfo',
            name='photo',
            field=models.ImageField(blank=True, default='carousel/Images/no-image.png', upload_to='author/profile'),
        ),
        migrations.AlterField(
            model_name='blogcontext',
            name='thumbnail',
            field=models.ImageField(blank=True, default='carousel/Images/no-image.png', upload_to='blog/thumbnails'),
        ),
        migrations.AlterField(
            model_name='blogimage',
            name='image',
            field=models.ImageField(blank=True, default='carousel/Images/no-image.png', upload_to='blog/Images'),
        ),
    ]
