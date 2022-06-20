# Generated by Django 3.2.11 on 2022-05-31 17:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('competitions', '0001_initial'),
        ('cart', '0006_remove_cart_cart'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartitem',
            name='cart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='cart.cart'),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='ticket',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='ticket_item', to='competitions.competitionticket'),
        ),
    ]
