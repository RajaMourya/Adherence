# Generated by Django 3.1.1 on 2020-09-21 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_auto_20200920_2107'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='age',
            field=models.IntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='gender',
            field=models.CharField(default='male', max_length=10),
            preserve_default=False,
        ),
    ]
