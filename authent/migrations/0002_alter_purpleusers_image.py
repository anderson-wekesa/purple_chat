# Generated by Django 4.1.2 on 2022-10-21 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authent', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purpleusers',
            name='image',
            field=models.ImageField(default='img/generic_user.jpg', upload_to='img'),
        ),
    ]
