# Generated by Django 5.0.6 on 2024-06-20 15:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tiktok', '0005_post_video_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='post',
            field=models.ForeignKey(default='', null=True, on_delete=django.db.models.deletion.CASCADE, to='tiktok.post'),
        ),
    ]
