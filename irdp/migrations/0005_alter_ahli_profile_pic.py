# Generated by Django 3.2.6 on 2021-08-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irdp', '0004_auto_20210830_0255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ahli',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
