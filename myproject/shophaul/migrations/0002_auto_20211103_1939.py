# Generated by Django 3.2.9 on 2021-11-03 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shophaul', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userregistration',
            name='id',
        ),
        migrations.AddField(
            model_name='userregistration',
            name='seller_id',
            field=models.AutoField(default='', primary_key=True, serialize=False),
        ),
    ]
