# Generated by Django 3.2.3 on 2021-07-16 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polling', '0006_extenduser_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extenduser',
            name='age',
            field=models.IntegerField(default=''),
        ),
    ]