# Generated by Django 4.2 on 2023-12-25 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInput',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('seed_text', models.CharField(max_length=255)),
                ('top_n', models.IntegerField(default=1)),
                ('prediction', models.TextField(blank=True)),
            ],
        ),
    ]
