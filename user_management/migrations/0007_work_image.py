# Generated by Django 4.2.5 on 2023-10-05 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_management', '0006_work'),
    ]

    operations = [
        migrations.AddField(
            model_name='work',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='work_posts'),
        ),
    ]