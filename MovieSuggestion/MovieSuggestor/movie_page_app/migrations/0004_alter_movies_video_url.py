# Generated by Django 5.2.3 on 2025-06-23 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie_page_app', '0003_movies_description_movies_rating_movies_video_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movies',
            name='video_url',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
