# Generated by Django 4.2 on 2024-10-13 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='group1',
            name='student',
            field=models.ManyToManyField(blank=True, related_name='groups', to='school.student'),
        ),
    ]
