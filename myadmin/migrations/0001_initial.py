# Generated by Django 2.2.3 on 2019-07-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoardPermission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('board_id', models.IntegerField(verbose_name='게시판 ID')),
                ('permission_type', models.IntegerField(choices=[(1, 'create'), (2, 'read'), (3, 'update'), (4, 'delete')], verbose_name='권한 대상')),
                ('permission_level', models.IntegerField(choices=[(1, 'user'), (2, 'admin'), (3, 'superuser')], verbose_name='권한')),
            ],
            options={
                'verbose_name': '패스트캠퍼스 권한',
                'verbose_name_plural': '패스트캠퍼스 권한',
                'db_table': 'fastcampus_board_permission',
            },
        ),
    ]
