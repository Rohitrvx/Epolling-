# Generated by Django 3.2.3 on 2021-07-19 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0009_auto_20210716_1905'),
    ]

    operations = [
        migrations.AddField(
            model_name='candidate',
            name='verifyimg',
            field=models.FileField(default=False, upload_to='images/'),
        ),
    ]
