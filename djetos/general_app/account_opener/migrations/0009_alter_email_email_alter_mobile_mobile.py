# Generated by Django 5.0.6 on 2024-07-03 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_opener', '0008_alter_email_email_alter_mobile_mobile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=250, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='mobile',
            name='mobile',
            field=models.CharField(max_length=15, primary_key=True, serialize=False, unique=True),
        ),
    ]
