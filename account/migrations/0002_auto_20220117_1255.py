# Generated by Django 3.2.9 on 2022-01-17 12:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='address2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_name',
        ),
        migrations.RemoveField(
            model_name='user',
            name='company_website',
        ),
    ]
