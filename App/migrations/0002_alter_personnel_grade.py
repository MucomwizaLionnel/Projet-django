# Generated by Django 5.0.7 on 2024-08-05 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personnel',
            name='grade',
            field=models.CharField(max_length=100, null=True),
        ),
    ]