# Generated by Django 3.1.1 on 2020-09-21 16:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200921_2132'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='plan',
        ),
    ]
