# Generated by Django 3.2.9 on 2021-11-18 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_auto_20211116_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardclient',
            name='nume',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='cardclient',
            name='prenume',
            field=models.TextField(),
        ),
    ]
