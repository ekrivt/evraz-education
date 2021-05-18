# Generated by Django 2.2.8 on 2021-05-17 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0003_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='author',
            field=models.CharField(max_length=50, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='task',
            name='performer',
            field=models.CharField(default=None, max_length=50, null=True, verbose_name='Исполнитель'),
        ),
    ]
