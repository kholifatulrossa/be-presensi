# Generated by Django 4.2.13 on 2024-10-09 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_user_guru_alter_user_siswa'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='token',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
