# Generated by Django 5.0.4 on 2024-05-01 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Vendor', '0004_remove_purchaseorder_issue_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='purchaseorder',
            old_name='ssue_date',
            new_name='issue_date',
        ),
    ]
