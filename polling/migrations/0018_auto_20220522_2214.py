# Generated by Django 3.2 on 2022-05-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0017_alter_extenduser_aadharphoto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='extenduser',
            name='aadharphoto',
        ),
        migrations.AlterField(
            model_name='aadhar',
            name='profile',
            field=models.FileField(default=False, upload_to='images/'),
        ),
    ]