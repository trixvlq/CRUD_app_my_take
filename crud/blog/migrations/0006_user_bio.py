# Generated by Django 4.2.6 on 2023-10-31 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]