# Generated by Django 3.2.11 on 2022-05-28 23:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0004_auto_20220529_0451'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cart',
            old_name='items',
            new_name='cart',
        ),
    ]