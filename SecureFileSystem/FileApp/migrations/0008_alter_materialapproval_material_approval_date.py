# Generated by Django 4.2.4 on 2023-08-24 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('FileApp', '0007_materialapproval'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialapproval',
            name='Material_Approval_Date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
