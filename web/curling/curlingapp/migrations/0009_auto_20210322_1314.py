# Generated by Django 3.1.7 on 2021-03-22 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('curlingapp', '0008_auto_20210322_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='camId',
            field=models.IntegerField(verbose_name='Sheet'),
        ),
    ]
