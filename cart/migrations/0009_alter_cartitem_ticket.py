# Generated by Django 3.2.11 on 2022-05-31 18:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
        ('cart', '0008_alter_cartitem_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cart_competition', to='competitions.competition'),
        ),
    ]
