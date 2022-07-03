# Generated by Django 4.0.5 on 2022-07-03 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('semesters', '0001_initial'),
        ('subjects', '0001_initial'),
        ('teams', '0001_initial'),
        ('teachers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendances',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timetable_detail_id', models.IntegerField(null=True)),
                ('student_id', models.IntegerField(null=True)),
                ('is_attended', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'attendances',
            },
        ),
        migrations.CreateModel(
            name='Shifts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_index', models.IntegerField(null=True)),
                ('start', models.CharField(max_length=150, null=True)),
                ('end', models.CharField(max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'shifts',
            },
        ),
        migrations.CreateModel(
            name='Timetables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('semester', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='semesters.semesters')),
                ('team', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teams.teams')),
            ],
            options={
                'db_table': 'timetables',
            },
        ),
        migrations.CreateModel(
            name='Timetable_requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.IntegerField(null=True)),
                ('block', models.IntegerField(null=True)),
                ('day_maximum', models.IntegerField(null=True)),
                ('week_maximum', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('timetable', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetables.timetables')),
            ],
            options={
                'db_table': 'timetable_requirements',
            },
        ),
        migrations.CreateModel(
            name='Timetable_details',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('shift', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetables.shifts')),
                ('subject', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='subjects.subjects')),
                ('teacher', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='teachers.teachers')),
                ('timetable', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetables.timetables')),
            ],
            options={
                'db_table': 'timetable_details',
            },
        ),
        migrations.CreateModel(
            name='Block_requirements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('block_number', models.IntegerField(null=True)),
                ('day_number', models.IntegerField(null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('required', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='timetables.timetable_requirements')),
            ],
            options={
                'db_table': 'block_requirements',
            },
        ),
    ]
