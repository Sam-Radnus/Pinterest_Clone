# Generated by Django 4.1.2 on 2022-11-01 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_remove_user_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='', null=True, upload_to=''),
        ),
    ]
