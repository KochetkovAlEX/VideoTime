# Generated by Django 5.0.6 on 2024-07-11 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mysite', '0002_video_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
