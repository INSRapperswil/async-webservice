# Generated by Django 3.0.7 on 2020-06-11 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('Created', 'Created'), ('Scheduled', 'Scheduled'), ('Running', 'Running'), ('Finished', 'Finished'), ('Failed', 'Failed'), ('Aborted', 'Aborted')], default='Created', max_length=20)),
                ('celery_task_id', models.CharField(blank=True, max_length=40)),
                ('started', models.DateTimeField(blank=True, null=True)),
                ('finished', models.DateTimeField(blank=True, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
