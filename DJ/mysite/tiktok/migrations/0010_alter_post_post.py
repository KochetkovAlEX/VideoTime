# Generated by Django 5.0.6 on 2024-06-27 15:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0009_alter_video_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='post',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
