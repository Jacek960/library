# Generated by Django 3.1.2 on 2020-10-09 17:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0005_auto_20201009_1506'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookhistoryrenting',
            name='book_instance',
            field=models.CharField(blank=True, max_length=36, null=True),
        ),
    ]
