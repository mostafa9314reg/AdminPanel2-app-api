# Generated by Django 4.2.2 on 2024-05-25 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Accounts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pcode', models.IntegerField()),
                ('extension', models.CharField(max_length=4, unique=True)),
                ('secret', models.CharField(max_length=20)),
                ('callerid', models.CharField(max_length=100)),
                ('mailbox', models.EmailField(max_length=50)),
                ('zones', models.CharField(blank=True, max_length=100, null=True)),
                ('level', models.CharField(max_length=50)),
                ('groups', models.CharField(blank=True, max_length=80, null=True)),
                ('cfwd', models.CharField(blank=True, max_length=30, null=True)),
                ('regione', models.CharField(blank=True, max_length=25, null=True)),
                ('server', models.CharField(max_length=50)),
                ('enable', models.IntegerField(db_column='Enable')),
                ('lastupdate', models.DateField(auto_now=True, db_column='LastUpdate', null=True)),
            ],
        ),
    ]
