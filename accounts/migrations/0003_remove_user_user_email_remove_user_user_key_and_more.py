# Generated by Django 4.1 on 2022-09-14 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_user_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='user_email',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_key',
        ),
        migrations.AddField(
            model_name='user',
            name='user_keyword3',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_auth_email',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_keyword1',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_keyword2',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_mbti',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_name',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_nickname',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.CharField(blank=True, default='0', max_length=50),
        ),
    ]
