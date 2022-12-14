# Generated by Django 4.1 on 2022-11-25 22:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0005_remove_follow_followed_alter_post_likes_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="follow",
            name="followed",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="followed",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="follow",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="following",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
