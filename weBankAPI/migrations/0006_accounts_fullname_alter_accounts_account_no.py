# Generated by Django 4.0.4 on 2022-04-28 01:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weBankAPI', '0005_transaction_account_balance_transaction_user_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='fullname',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='accounts',
            name='account_no',
            field=models.IntegerField(unique=True),
        ),
    ]
