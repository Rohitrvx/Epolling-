# Generated by Django 3.2 on 2022-05-22 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0015_auto_20220522_2137'),
    ]

    operations = [
        migrations.AddField(
            model_name='extenduser',
            name='aadharphoto',
            field=models.FileField(default=False, upload_to=''),
        ),
    ]
