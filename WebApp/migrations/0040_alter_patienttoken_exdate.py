# Generated by Django 3.2.9 on 2021-11-30 16:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebApp', '0039_alter_patienttoken_exdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patienttoken',
            name='exdate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]