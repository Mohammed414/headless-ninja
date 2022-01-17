# Generated by Django 3.2.9 on 2022-01-16 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0005_alter_article_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='language',
            field=models.CharField(choices=[('ar', 'Arabic'), ('en', 'English')], default='ar', max_length=7),
        ),
    ]
