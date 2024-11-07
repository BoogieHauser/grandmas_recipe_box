# Generated by Django 5.1.3 on 2024-11-07 02:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('ingredients', models.TextField()),
                ('instructions', models.TextField()),
                ('prepMinutes', models.IntegerField()),
                ('cookMinutes', models.IntegerField()),
                ('servings', models.IntegerField()),
            ],
        ),
    ]
