# Generated by Django 3.0 on 2019-12-15 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0010_transaction_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bot.Profile', to_field='user_id'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user_id',
            field=models.PositiveIntegerField(unique=True),
        ),
    ]
