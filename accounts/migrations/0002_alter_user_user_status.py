# Generated by Django 4.1 on 2022-08-12 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_status',
            field=models.CharField(blank=None, default='0', max_length=50, null=True),
        ),
    ]