# Generated by Django 4.1.2 on 2022-11-18 03:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_post_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='caption',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
