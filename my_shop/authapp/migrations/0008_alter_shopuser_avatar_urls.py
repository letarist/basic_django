# Generated by Django 3.2.8 on 2021-11-23 16:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_shopuser_avatar_urls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuser',
            name='avatar_urls',
            field=models.URLField(blank=True, max_length=128, null=True, verbose_name='Аватар'),
        ),
    ]
