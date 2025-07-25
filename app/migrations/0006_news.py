# Generated by Django 5.2.4 on 2025-07-14 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_remove_userprofile_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('announcement', 'Анонс'), ('security', 'Безопасность'), ('update', 'Обновление')], max_length=20)),
            ],
        ),
    ]
