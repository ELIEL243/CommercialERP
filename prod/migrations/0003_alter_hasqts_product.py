# Generated by Django 4.2.2 on 2023-07-03 04:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appro', '0003_alter_product_img'),
        ('prod', '0002_operationpt_orderprod_orderpv_rename_haspf_hasqts_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hasqts',
            name='product',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='appro.product'),
        ),
    ]
