# Generated by Django 3.2.18 on 2023-04-25 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eventhost', '0006_alter_eventrequest_eventname'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='contract_address',
            new_name='address',
        ),
    ]
