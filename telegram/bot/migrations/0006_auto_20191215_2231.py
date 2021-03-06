# Generated by Django 3.0 on 2019-12-15 17:31

import bot.models
import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0005_auto_20191215_1053'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.PositiveIntegerField()),
                ('first_name', models.CharField(blank=True, max_length=450, null=True)),
                ('last_name', models.CharField(blank=True, max_length=450, null=True)),
                ('username', models.CharField(blank=True, max_length=450, null=True)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('created_on', models.DateTimeField(default=datetime.datetime.now)),
                ('invited_by', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.Profile')),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profiles',
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('card', models.CharField(blank=True, max_length=200, null=True)),
                ('type', models.CharField(choices=[('V', 'Вывод'), ('P', 'Пополнение')], max_length=1)),
                ('sum', models.PositiveIntegerField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, upload_to=bot.models.image_folder)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('broker', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.Profile')),
            ],
            options={
                'verbose_name': 'Transaction',
                'verbose_name_plural': 'Transactions',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='VerifiedTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('verified_sum', models.DecimalField(decimal_places=2, max_digits=10)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('transaction', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='bot.Transaction')),
            ],
            options={
                'verbose_name': 'VerifiedTransaction',
                'verbose_name_plural': 'VerifiedTransactions',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.DeleteModel(
            name='Profiles',
        ),
    ]
