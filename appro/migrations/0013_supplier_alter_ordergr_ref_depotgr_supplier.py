# Generated by Django 4.2.2 on 2023-10-27 03:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('appro', '0012_alter_ordergr_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Supplier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('mail', models.EmailField(max_length=254, null=True)),
                ('adress', models.TextField()),
            ],
        ),
        migrations.AlterField(
            model_name='ordergr',
            name='ref',
            field=models.CharField(default='6b3981fb47', max_length=10),
        ),
        migrations.AddField(
            model_name='depotgr',
            name='supplier',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='appro.supplier'),
        ),
    ]