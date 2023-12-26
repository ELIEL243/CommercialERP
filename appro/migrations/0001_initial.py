# Generated by Django 4.2.2 on 2023-06-30 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DepotGr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='LivraisonGr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qts', models.DecimalField(decimal_places=2, default=1, max_digits=10)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(null=True, upload_to='products-images')),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('type_product', models.CharField(choices=[('matière première', 'produit fini'), ('matière première', 'produit fini')], max_length=255)),
                ('qts', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Operation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_operation', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('livraison', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appro.livraisongr')),
                ('reception', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appro.depotgr')),
            ],
        ),
        migrations.AddField(
            model_name='livraisongr',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appro.product'),
        ),
        migrations.AddField(
            model_name='depotgr',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='appro.product'),
        ),
    ]
