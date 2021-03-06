# Generated by Django 3.1.7 on 2021-03-25 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_listing_watchlisted_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AlterField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]
