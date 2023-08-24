# Generated by Django 4.2.4 on 2023-08-24 05:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('FileApp', '0006_alter_material_material_contributor'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialApproval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Approval_Status', models.CharField(choices=[('YES', 'YES'), ('NO', 'NO'), ('---', '---')], default='---', max_length=20)),
                ('Material_Approval_Request_Date', models.DateTimeField(auto_now_add=True)),
                ('Material_Approval_Date', models.DateTimeField()),
                ('Material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='FileApp.material', verbose_name='Material')),
                ('Requested_User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Requested User')),
            ],
            options={
                'verbose_name_plural': 'Material Approval',
            },
        ),
    ]