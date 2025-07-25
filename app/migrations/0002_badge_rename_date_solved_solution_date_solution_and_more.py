# Generated by Django 5.2.4 on 2025-07-06 08:45

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('color', models.IntegerField(choices=[(0, 'Green'), (1, 'Blue'), (2, 'Yellow'), (3, 'Purple'), (4, 'Red')])),
            ],
        ),
        migrations.RenameField(
            model_name='solution',
            old_name='date_solved',
            new_name='date_solution',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='tasks',
        ),
        migrations.AlterField(
            model_name='solution',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.task'),
        ),
        migrations.AlterField(
            model_name='solution',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='solutions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='task',
            name='complexity',
            field=models.IntegerField(choices=[(0, 'Easy'), (1, 'Medium'), (2, 'Hard'), (3, 'Extreme'), (4, 'Hardcore')]),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='badges',
            field=models.ManyToManyField(blank=True, to='app.badge'),
        ),
    ]
