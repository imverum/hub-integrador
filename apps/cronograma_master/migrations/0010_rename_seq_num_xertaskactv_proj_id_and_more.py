# Generated by Django 4.1.7 on 2023-04-24 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cronograma_master', '0009_alter_stagecronogramamaster_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='xertaskactv',
            old_name='seq_num',
            new_name='proj_id',
        ),
        migrations.RemoveField(
            model_name='xertaskactv',
            name='actv_code_name',
        ),
        migrations.RemoveField(
            model_name='xertaskactv',
            name='parent_actv_code_id',
        ),
        migrations.RemoveField(
            model_name='xertaskactv',
            name='short_name',
        ),
        migrations.AddField(
            model_name='xertaskactv',
            name='task_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
