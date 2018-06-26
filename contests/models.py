import datetime
from django.db import models
from users.models import *
from problems.models import *
"""Модели для работы с контестами"""


# Таблица для хранения контестов
class Contests(models.Model):
    name = models.CharField(null=False, max_length=40, verbose_name="Название")
    full_id = models.CharField(null=False, unique=True, max_length=10, verbose_name="Полный ID")
    sched_time = models.DateTimeField(null=True, verbose_name="Дата начала")
    duration = models.IntegerField(null=True, blank=True, verbose_name="Длительность в минутах")
    contest_dir = models.CharField(null=True, max_length=256, verbose_name="Путь к папке с контестом")
    xml_config_path = models.CharField(null=True, max_length=256, verbose_name="Путь к XML файлу конфигурации")
    config_path = models.CharField(null=True, max_length=256, verbose_name="Путь к файлу конфигурации serve.cfg")
    problems = models.TextField(default='', blank=True, verbose_name="JSON со списком задач")

    def __str__(self):
        return "%s" % self.name

    class Meta:
        db_table = 'contests'
        verbose_name = 'Контест'
        verbose_name_plural = 'Контесты'


# Хз пока что это
class Clars(models.Model):
    clar_id = models.IntegerField(primary_key=True)
    uuid = models.CharField(unique=True, max_length=40)
    contest_id = models.IntegerField()
    size = models.IntegerField()
    create_time = models.DateTimeField()
    nsec = models.IntegerField()
    user_from = models.IntegerField()
    user_to = models.IntegerField()
    j_from = models.IntegerField()
    flags = models.IntegerField()
    ip_version = models.IntegerField()
    hide_flag = models.IntegerField()
    ssl_flag = models.IntegerField()
    appeal_flag = models.IntegerField()
    ip = models.CharField(max_length=64)
    locale_id = models.IntegerField()
    in_reply_to = models.IntegerField()
    in_reply_uuid = models.CharField(max_length=40, blank=True, null=True)
    run_id = models.IntegerField()
    run_uuid = models.CharField(max_length=40, blank=True, null=True)
    old_run_status = models.IntegerField()
    new_run_status = models.IntegerField()
    clar_charset = models.CharField(max_length=32, blank=True, null=True)
    subj = models.CharField(max_length=128, blank=True, null=True)

    class Meta:
        db_table = 'clars'
        unique_together = (('clar_id', 'contest_id'),)


# Какая-то таблица связи
class Clartexts(models.Model):
    clar_id = models.IntegerField(primary_key=True)
    contest_id = models.IntegerField()
    uuid = models.CharField(unique=True, max_length=40)
    clar_text = models.CharField(max_length=4096, blank=True, null=True)

    class Meta:
        db_table = 'clartexts'
        unique_together = (('clar_id', 'contest_id'),)

# Регистрация на контесты
class Cntsregs(models.Model):
    user = models.ForeignKey('users.Logins', on_delete=models.CASCADE, primary_key=True)
    contest_id = models.IntegerField()
    status = models.IntegerField(default=0)
    banned = models.IntegerField(default=0)
    invisible = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    incomplete = models.IntegerField(default=0)
    disqualified = models.IntegerField(default=0)
    createtime = models.DateTimeField(auto_now_add=True, blank=True)
    changetime = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        db_table = 'cntsregs'
        unique_together = (('user', 'contest_id'),)


# Конфигурационные данные
class Config(models.Model):
    config_key = models.CharField(primary_key=True, max_length=64)
    config_val = models.CharField(max_length=64, blank=True, null=True)

    class Meta:
        db_table = 'config'


# Куки
class Cookies(models.Model):
    cookie = models.CharField(primary_key=True, max_length=64)
    user = models.ForeignKey('users.Logins', models.DO_NOTHING)
    contest_id = models.IntegerField()
    priv_level = models.IntegerField()
    role_id = models.IntegerField()
    ip_version = models.IntegerField()
    locale_id = models.IntegerField()
    recovery = models.IntegerField()
    team_login = models.IntegerField()
    ip = models.CharField(max_length=64)
    ssl_flag = models.IntegerField()
    expire = models.DateTimeField()

    class Meta:
        db_table = 'cookies'


# Запущенные контесты
class Runheaders(models.Model):
    contest_id = models.IntegerField(primary_key=True)
    start_time = models.DateTimeField()
    sched_time = models.DateTimeField()
    duration = models.IntegerField(blank=True, null=True)
    stop_time = models.DateTimeField()
    finish_time = models.DateTimeField()
    saved_duration = models.IntegerField(blank=True, null=True)
    saved_stop_time = models.DateTimeField()
    saved_finish_time = models.DateTimeField()
    last_change_time = models.DateTimeField()
    last_change_nsec = models.IntegerField()
    next_run_id = models.IntegerField()

    class Meta:
        db_table = 'runheaders'


# Информация о пользователях в запущенном контесте
class Runs(models.Model):
    run_id = models.IntegerField(primary_key=True)
    contest_id = models.IntegerField()
    size = models.IntegerField()
    create_time = models.DateTimeField()
    create_nsec = models.IntegerField()
    user_id = models.IntegerField()
    prob_id = models.IntegerField()
    lang_id = models.IntegerField()
    status = models.IntegerField()
    ssl_flag = models.IntegerField()
    ip_version = models.IntegerField()
    ip = models.CharField(max_length=64)
    hash = models.CharField(max_length=128, blank=True, null=True)
    run_uuid = models.CharField(max_length=40, blank=True, null=True)
    score = models.IntegerField()
    test_num = models.IntegerField()
    score_adj = models.IntegerField()
    locale_id = models.IntegerField()
    judge_id = models.IntegerField()
    variant = models.IntegerField()
    pages = models.IntegerField()
    is_imported = models.IntegerField()
    is_hidden = models.IntegerField()
    is_readonly = models.IntegerField()
    is_examinable = models.IntegerField()
    mime_type = models.CharField(max_length=64, blank=True, null=True)
    examiners0 = models.IntegerField()
    examiners1 = models.IntegerField()
    examiners2 = models.IntegerField()
    exam_score0 = models.IntegerField()
    exam_score1 = models.IntegerField()
    exam_score2 = models.IntegerField()
    last_change_time = models.DateTimeField()
    last_change_nsec = models.IntegerField()
    is_marked = models.IntegerField()
    is_saved = models.IntegerField()
    saved_status = models.IntegerField()
    saved_score = models.IntegerField()
    saved_test = models.IntegerField()
    passed_mode = models.IntegerField()
    eoln_type = models.IntegerField()
    store_flags = models.IntegerField()
    token_flags = models.IntegerField()
    token_count = models.IntegerField()

    class Meta:
        db_table = 'runs'
        unique_together = (('run_id', 'contest_id'),)