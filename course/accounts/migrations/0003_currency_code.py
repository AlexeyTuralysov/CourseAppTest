# Generated by Django 5.1.4 on 2024-12-17 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_rename_exchange_rate_currency_course_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='currency',
            name='code',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]