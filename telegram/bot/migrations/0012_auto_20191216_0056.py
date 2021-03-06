# Generated by Django 3.0 on 2019-12-15 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0011_auto_20191216_0001'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='invited_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='bot.Profile'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='broker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.Profile', to_field='user_id'),
        ),
    ]
