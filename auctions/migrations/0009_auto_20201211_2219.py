# Generated by Django 3.1.3 on 2020-12-11 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_watchlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='auction',
            field=models.ManyToManyField(to='auctions.Auctions'),
        ),
    ]
