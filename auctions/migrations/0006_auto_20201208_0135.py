# Generated by Django 3.1.3 on 2020-12-07 19:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_auto_20201204_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='auction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auctions'),
        ),
    ]