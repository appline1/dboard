# Generated by Django 4.1.5 on 2023-02-18 04:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accts', '0003_alter_mybank_acctno'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MyBank',
            new_name='BankAccount',
        ),
    ]
