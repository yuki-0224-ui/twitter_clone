# Generated by Django 4.2.5 on 2025-01-06 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tweets', '0006_tweet_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tweet',
            name='content',
            field=models.CharField(blank=True, max_length=140, null=True),
        ),
    ]
