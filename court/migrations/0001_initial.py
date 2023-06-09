# Generated by Django 4.2 on 2023-04-19 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Court',
            fields=[
                ('courtID', models.IntegerField(primary_key=True, serialize=False)),
                ('x', models.DecimalField(decimal_places=6, max_digits=9)),
                ('y', models.DecimalField(decimal_places=6, max_digits=9)),
                ('city', models.CharField(max_length=50)),
                ('neighborhood', models.CharField(max_length=50)),
                ('max_players', models.PositiveIntegerField()),
            ],
        ),
    ]
