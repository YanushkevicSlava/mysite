# Generated by Django 4.2.1 on 2023-07-20 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopapp', '0010_productimage'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Order', 'verbose_name_plural': 'Orders'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Product', 'verbose_name_plural': 'Products'},
        ),
    ]
