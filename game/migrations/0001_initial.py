# Generated by Django 2.2.1 on 2019-09-26 17:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game_id', models.CharField(max_length=10)),
                ('player_name', models.CharField(max_length=100)),
                ('status', models.IntegerField()),
                ('winner', models.IntegerField()),
                ('active_player', models.IntegerField()),
                ('turns_played', models.IntegerField()),
                ('y_tower', models.IntegerField()),
                ('y_wall', models.IntegerField()),
                ('o_tower', models.IntegerField()),
                ('o_wall', models.IntegerField()),
                ('y_coffee', models.IntegerField()),
                ('y_javas', models.IntegerField()),
                ('y_mines', models.IntegerField()),
                ('y_rubies', models.IntegerField()),
                ('y_dungeons', models.IntegerField()),
                ('y_pythons', models.IntegerField()),
                ('o_coffee', models.IntegerField()),
                ('o_javas', models.IntegerField()),
                ('o_mines', models.IntegerField()),
                ('o_rubies', models.IntegerField()),
                ('o_dungeons', models.IntegerField()),
                ('o_pythons', models.IntegerField()),
                ('y_cards', models.CharField(max_length=50)),
                ('await', models.CharField(max_length=10)),
                ('after_await', models.CharField(max_length=100)),
                ('y_last_card', models.IntegerField()),
                ('o_last_card', models.IntegerField()),
            ],
        ),
    ]
