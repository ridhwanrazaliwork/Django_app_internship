# Generated by Django 3.2.6 on 2021-08-29 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('irdp', '0005_alter_ahli_profile_pic'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ahli',
            name='profile_pic',
        ),
        migrations.AddField(
            model_name='ahli',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='profile_images/'),
        ),
    ]