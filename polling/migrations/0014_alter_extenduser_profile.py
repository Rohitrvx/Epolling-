# Generated by Django 3.2 on 2022-05-22 15:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0013_alter_extenduser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='profile',
            field=models.FileField(default=False, upload_to=''),
        ),
    ]
