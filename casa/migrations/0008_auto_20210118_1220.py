# Generated by Django 3.1.4 on 2021-01-18 10:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casa', '0007_auto_20210117_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='receipt',
            name='receipt_no',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
