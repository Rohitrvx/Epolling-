# Generated by Django 3.2 on 2022-05-22 13:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0010_candidate_verifyimg'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='profile',
            field=models.FileField(default=False, upload_to='media/images/'),
        ),
    ]
