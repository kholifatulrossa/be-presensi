# Generated by Django 4.2.13 on 2024-10-14 01:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_alter_guru_nip_alter_siswa_nisn'),
    ]

    operations = [
        migrations.AddField(
            model_name='kehadiran',
            name='keterangan',
            field=models.TextField(max_length=1000, null=True),
        ),
    ]
