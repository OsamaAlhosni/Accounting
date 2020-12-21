# Generated by Django 3.1.4 on 2020-12-17 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_name', models.CharField(max_length=200)),
                ('beginig_balance', models.DecimalField(blank=True, decimal_places=3, max_digits=19, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
    ]
