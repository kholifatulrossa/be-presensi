# Generated by Django 4.2.13 on 2024-10-09 02:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_alter_kehadiran_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guru',
            old_name='kelasId',
            new_name='kelas',
        ),
        migrations.RenameField(
            model_name='kehadiran',
            old_name='siswaId',
            new_name='siswa',
        ),
        migrations.RenameField(
            model_name='siswa',
            old_name='kelasId',
            new_name='kelas',
        ),
    ]
