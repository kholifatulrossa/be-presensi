# Generated by Django 4.2.13 on 2024-10-17 01:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_alter_user_guru_alter_user_siswa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kehadiran',
            name='tanggal',
            field=models.CharField(max_length=50),
        ),
    ]
