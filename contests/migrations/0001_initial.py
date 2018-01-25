# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-25 03:51
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Clars',
            fields=[
                ('clar_id', models.IntegerField(primary_key=True, serialize=False)),
                ('uuid', models.CharField(max_length=40, unique=True)),
                ('contest_id', models.IntegerField()),
                ('size', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('nsec', models.IntegerField()),
                ('user_from', models.IntegerField()),
                ('user_to', models.IntegerField()),
                ('j_from', models.IntegerField()),
                ('flags', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('hide_flag', models.IntegerField()),
                ('ssl_flag', models.IntegerField()),
                ('appeal_flag', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('locale_id', models.IntegerField()),
                ('in_reply_to', models.IntegerField()),
                ('in_reply_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('run_id', models.IntegerField()),
                ('run_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('old_run_status', models.IntegerField()),
                ('new_run_status', models.IntegerField()),
                ('clar_charset', models.CharField(blank=True, max_length=32, null=True)),
                ('subj', models.CharField(blank=True, max_length=128, null=True)),
            ],
            options={
                'db_table': 'clars',
            },
        ),
        migrations.CreateModel(
            name='Clartexts',
            fields=[
                ('clar_id', models.IntegerField(primary_key=True, serialize=False)),
                ('contest_id', models.IntegerField()),
                ('uuid', models.CharField(max_length=40, unique=True)),
                ('clar_text', models.CharField(blank=True, max_length=4096, null=True)),
            ],
            options={
                'db_table': 'clartexts',
            },
        ),
        migrations.CreateModel(
            name='Cntsregs',
            fields=[
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, primary_key=True, serialize=False, to='users.Logins')),
                ('contest_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('banned', models.IntegerField()),
                ('invisible', models.IntegerField()),
                ('locked', models.IntegerField()),
                ('incomplete', models.IntegerField()),
                ('disqualified', models.IntegerField()),
                ('createtime', models.DateTimeField()),
                ('changetime', models.DateTimeField()),
            ],
            options={
                'db_table': 'cntsregs',
            },
        ),
        migrations.CreateModel(
            name='Config',
            fields=[
                ('config_key', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('config_val', models.CharField(blank=True, max_length=64, null=True)),
            ],
            options={
                'db_table': 'config',
            },
        ),
        migrations.CreateModel(
            name='Cookies',
            fields=[
                ('cookie', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('contest_id', models.IntegerField()),
                ('priv_level', models.IntegerField()),
                ('role_id', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('locale_id', models.IntegerField()),
                ('recovery', models.IntegerField()),
                ('team_login', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('ssl_flag', models.IntegerField()),
                ('expire', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='users.Logins')),
            ],
            options={
                'db_table': 'cookies',
            },
        ),
        migrations.CreateModel(
            name='Runheaders',
            fields=[
                ('contest_id', models.IntegerField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('sched_time', models.DateTimeField()),
                ('duration', models.IntegerField(blank=True, null=True)),
                ('stop_time', models.DateTimeField()),
                ('finish_time', models.DateTimeField()),
                ('saved_duration', models.IntegerField(blank=True, null=True)),
                ('saved_stop_time', models.DateTimeField()),
                ('saved_finish_time', models.DateTimeField()),
                ('last_change_time', models.DateTimeField()),
                ('last_change_nsec', models.IntegerField()),
                ('next_run_id', models.IntegerField()),
            ],
            options={
                'db_table': 'runheaders',
            },
        ),
        migrations.CreateModel(
            name='Runs',
            fields=[
                ('run_id', models.IntegerField(primary_key=True, serialize=False)),
                ('contest_id', models.IntegerField()),
                ('size', models.IntegerField()),
                ('create_time', models.DateTimeField()),
                ('create_nsec', models.IntegerField()),
                ('user_id', models.IntegerField()),
                ('prob_id', models.IntegerField()),
                ('lang_id', models.IntegerField()),
                ('status', models.IntegerField()),
                ('ssl_flag', models.IntegerField()),
                ('ip_version', models.IntegerField()),
                ('ip', models.CharField(max_length=64)),
                ('hash', models.CharField(blank=True, max_length=128, null=True)),
                ('run_uuid', models.CharField(blank=True, max_length=40, null=True)),
                ('score', models.IntegerField()),
                ('test_num', models.IntegerField()),
                ('score_adj', models.IntegerField()),
                ('locale_id', models.IntegerField()),
                ('judge_id', models.IntegerField()),
                ('variant', models.IntegerField()),
                ('pages', models.IntegerField()),
                ('is_imported', models.IntegerField()),
                ('is_hidden', models.IntegerField()),
                ('is_readonly', models.IntegerField()),
                ('is_examinable', models.IntegerField()),
                ('mime_type', models.CharField(blank=True, max_length=64, null=True)),
                ('examiners0', models.IntegerField()),
                ('examiners1', models.IntegerField()),
                ('examiners2', models.IntegerField()),
                ('exam_score0', models.IntegerField()),
                ('exam_score1', models.IntegerField()),
                ('exam_score2', models.IntegerField()),
                ('last_change_time', models.DateTimeField()),
                ('last_change_nsec', models.IntegerField()),
                ('is_marked', models.IntegerField()),
                ('is_saved', models.IntegerField()),
                ('saved_status', models.IntegerField()),
                ('saved_score', models.IntegerField()),
                ('saved_test', models.IntegerField()),
                ('passed_mode', models.IntegerField()),
                ('eoln_type', models.IntegerField()),
                ('store_flags', models.IntegerField()),
                ('token_flags', models.IntegerField()),
                ('token_count', models.IntegerField()),
            ],
            options={
                'db_table': 'runs',
            },
        ),
        migrations.AlterUniqueTogether(
            name='runs',
            unique_together=set([('run_id', 'contest_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='cntsregs',
            unique_together=set([('user', 'contest_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='clartexts',
            unique_together=set([('clar_id', 'contest_id')]),
        ),
        migrations.AlterUniqueTogether(
            name='clars',
            unique_together=set([('clar_id', 'contest_id')]),
        ),
    ]
