# Generated by Django 2.2.6 on 2020-12-16 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201215_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='status',
            field=models.CharField(blank=True, default='У меня ещё нет статуса, но когда-то должен появиться', max_length=200, verbose_name='Статус'),
        ),
    ]