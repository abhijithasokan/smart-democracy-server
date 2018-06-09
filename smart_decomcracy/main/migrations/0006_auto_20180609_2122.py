# Generated by Django 2.0.3 on 2018-06-09 21:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180609_1916'),
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option_num', models.PositiveIntegerField()),
                ('choice_name', models.CharField(max_length=30)),
                ('votes', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('poll_id', models.AutoField(primary_key=True, serialize=False)),
                ('official', models.BooleanField(default=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('heading', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('vote_count', models.PositiveIntegerField(default=0)),
                ('closed', models.BooleanField(default=False)),
                ('constituency', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Constituency')),
                ('creator', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.User')),
            ],
        ),
        migrations.AddField(
            model_name='option',
            name='poll',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.Poll'),
        ),
    ]
