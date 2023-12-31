# Generated by Django 4.2.2 on 2023-07-03 04:38

from django.db import migrations, models
import django.db.models.deletion
import prod.models


class Migration(migrations.Migration):

    dependencies = [
        ('appro', '0003_alter_product_img'),
        ('prod', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OperationPt',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type_operation', models.CharField(max_length=10, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('livraison', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prod.livraisonprod')),
                ('livraison_pv', models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='livraison_pv', to='prod.livraisonpv')),
                ('reception', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prod.depotpt')),
            ],
        ),
        migrations.CreateModel(
            name='OrderProd',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(default=prod.models.generate_unique_uid, max_length=10, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='OrderPv',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ref', models.CharField(default=prod.models.generate_unique_uid, max_length=10, unique=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.RenameModel(
            old_name='HasPf',
            new_name='HasQts',
        ),
        migrations.DeleteModel(
            name='HasMP',
        ),
        migrations.AddField(
            model_name='livraisonprod',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='prod.orderprod'),
        ),
        migrations.AddField(
            model_name='livraisonpv',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='prod.orderpv'),
        ),
    ]
