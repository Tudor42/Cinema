# Generated by Django 3.2.9 on 2021-12-06 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0004_alter_cardclient_puncte'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardclient',
            name='puncte',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='film',
            name='pret',
            field=models.PositiveIntegerField(),
        ),
    ]
