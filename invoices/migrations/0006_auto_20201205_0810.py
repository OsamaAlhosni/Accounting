# Generated by Django 3.1.4 on 2020-12-05 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('invoices', '0005_auto_20201205_0716'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='Invoice_no',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='balance_to',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='from_date',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='invoice_amount',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='invoice',
            name='proid',
        ),
    ]
