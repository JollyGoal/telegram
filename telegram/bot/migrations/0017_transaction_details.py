# Generated by Django 3.0 on 2019-12-26 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0016_auto_20191226_1156'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='details',
            field=models.TextField(blank=True, null=True),
        ),
    ]
