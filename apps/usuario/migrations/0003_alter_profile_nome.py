# Generated by Django 4.1.1 on 2022-11-08 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_remove_profile_whatsapp_profile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='nome',
            field=models.CharField(blank=True, max_length=300, null=True),
        ),
    ]