# Generated by Django 4.2.2 on 2023-11-14 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appro', '0018_ordercmd_shipped_alter_ordercmd_ref_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordercmd',
            name='ref',
            field=models.CharField(default='6236dfe3b7', max_length=10),
        ),
        migrations.AlterField(
            model_name='ordergr',
            name='ref',
            field=models.CharField(default='27235f7d0f', max_length=10),
        ),
    ]