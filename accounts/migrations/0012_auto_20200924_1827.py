# Generated by Django 3.1.1 on 2020-09-24 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_auto_20200924_1649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='emergency',
            field=models.EmailField(max_length=10),
        ),
    ]