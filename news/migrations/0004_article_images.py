# Generated by Django 3.2.9 on 2022-03-01 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_article_title'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='images',
            field=models.ManyToManyField(blank=True, to='news.Image'),
        ),
    ]
