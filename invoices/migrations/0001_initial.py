# Generated by Django 3.1.4 on 2020-12-04 08:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_id', models.IntegerField()),
                ('customer_name', models.CharField(blank=True, max_length=200, null=True)),
                ('balance', models.DecimalField(decimal_places=3, max_digits=7)),
                ('from_date', models.DateField(blank=True, null=True)),
                ('balance_to', models.DateField(blank=True, default=0, null=True)),
                ('proid', models.IntegerField(default=0)),
                ('Invoice_no', models.CharField(blank=True, max_length=30, null=True)),
                ('invoice_amount', models.DecimalField(decimal_places=3, default=0.0, max_digits=7)),
                ('upload_date', models.DateTimeField(auto_now=True)),
                ('notes', models.CharField(blank=True, max_length=200, null=True)),
            ],
        ),
    ]
