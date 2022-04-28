# Generated by Django 4.0.4 on 2022-04-28 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('weBankAPI', '0004_remove_user_otp'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='account_balance',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='otp',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
