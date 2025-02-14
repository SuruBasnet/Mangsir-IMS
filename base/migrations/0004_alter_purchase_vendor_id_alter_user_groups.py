# Generated by Django 5.1.5 on 2025-02-04 01:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('base', '0003_remove_user_groups_user_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='vendor_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.vendor'),
        ),
        migrations.AlterField(
            model_name='user',
            name='groups',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='auth.group'),
        ),
    ]
