# Generated by Django 3.2.11 on 2022-05-31 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0010_auto_20220531_2354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='competition',
        ),
    ]
