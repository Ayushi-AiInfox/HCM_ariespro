# Generated by Django 3.2.15 on 2022-09-26 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainlogin', '0002_alter_login_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usertype',
            options={'managed': True},
        ),
    ]