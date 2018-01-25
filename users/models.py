from __future__ import unicode_literals
from django.db import models

"""Модели для работы с пользователями в системе Ejudge"""


# Модель данных для входа пользователей
class Logins(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=64)
    email = models.CharField(max_length=128, blank=True, null=True)
    pwdmethod = models.IntegerField(default=2)
    password = models.CharField(max_length=128, blank=True, null=True)
    privileged = models.IntegerField(default=0)
    invisible = models.IntegerField(default=0)
    banned = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    readonly = models.IntegerField(default=0)
    neverclean = models.IntegerField(default=0)
    simplereg = models.IntegerField(default=0)
    regtime = models.DateTimeField(auto_now_add=True, blank=True)
    logintime = models.DateTimeField(auto_now_add=True, blank=True)
    pwdtime = models.DateTimeField(auto_now_add=True, blank=True)
    changetime = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return "%s" % self.login

    class Meta:
        db_table = 'logins'
        ordering = ['user_id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'




# Модель данных о пользователях
class Users(models.Model):
    user = models.ForeignKey('Logins', models.DO_NOTHING, primary_key=True)
    contest_id = models.IntegerField()
    cnts_read_only = models.IntegerField()
    instnum = models.IntegerField(blank=True, null=True)
    username = models.CharField(max_length=512, blank=True, null=True)
    pwdmethod = models.IntegerField()
    password = models.CharField(max_length=128, blank=True, null=True)
    pwdtime = models.DateTimeField()
    createtime = models.DateTimeField()
    changetime = models.DateTimeField()
    logintime = models.DateTimeField()
    inst = models.CharField(max_length=512, blank=True, null=True)
    inst_en = models.CharField(max_length=512, blank=True, null=True)
    instshort = models.CharField(max_length=512, blank=True, null=True)
    instshort_en = models.CharField(max_length=512, blank=True, null=True)
    fac = models.CharField(max_length=512, blank=True, null=True)
    fac_en = models.CharField(max_length=512, blank=True, null=True)
    facshort = models.CharField(max_length=512, blank=True, null=True)
    facshort_en = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=512, blank=True, null=True)
    city = models.CharField(max_length=512, blank=True, null=True)
    city_en = models.CharField(max_length=512, blank=True, null=True)
    region = models.CharField(max_length=512, blank=True, null=True)
    area = models.CharField(max_length=512, blank=True, null=True)
    zip = models.CharField(max_length=512, blank=True, null=True)
    street = models.CharField(max_length=512, blank=True, null=True)
    country = models.CharField(max_length=512, blank=True, null=True)
    country_en = models.CharField(max_length=512, blank=True, null=True)
    location = models.CharField(max_length=512, blank=True, null=True)
    spelling = models.CharField(max_length=512, blank=True, null=True)
    printer = models.CharField(max_length=512, blank=True, null=True)
    languages = models.CharField(max_length=512, blank=True, null=True)
    exam_id = models.CharField(max_length=512, blank=True, null=True)
    exam_cypher = models.CharField(max_length=512, blank=True, null=True)
    field0 = models.CharField(max_length=512, blank=True, null=True)
    field1 = models.CharField(max_length=512, blank=True, null=True)
    field2 = models.CharField(max_length=512, blank=True, null=True)
    field3 = models.CharField(max_length=512, blank=True, null=True)
    field4 = models.CharField(max_length=512, blank=True, null=True)
    field5 = models.CharField(max_length=512, blank=True, null=True)
    field6 = models.CharField(max_length=512, blank=True, null=True)
    field7 = models.CharField(max_length=512, blank=True, null=True)
    field8 = models.CharField(max_length=512, blank=True, null=True)
    field9 = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'users'
        unique_together = (('user', 'contest_id'),)


# Информация о членах команды или личная информация индив. участников
class Members(models.Model):
    serial = models.AutoField(primary_key=True)
    user = models.ForeignKey('Logins', models.DO_NOTHING)
    contest_id = models.IntegerField()
    role_id = models.IntegerField()
    createtime = models.DateTimeField()
    changetime = models.DateTimeField()
    firstname = models.CharField(max_length=512, blank=True, null=True)
    firstname_en = models.CharField(max_length=512, blank=True, null=True)
    middlename = models.CharField(max_length=512, blank=True, null=True)
    middlename_en = models.CharField(max_length=512, blank=True, null=True)
    surname = models.CharField(max_length=512, blank=True, null=True)
    surname_en = models.CharField(max_length=512, blank=True, null=True)
    status = models.IntegerField()
    gender = models.IntegerField()
    grade = models.IntegerField()
    grp = models.CharField(max_length=512, blank=True, null=True)
    grp_en = models.CharField(max_length=512, blank=True, null=True)
    occupation = models.CharField(max_length=512, blank=True, null=True)
    occupation_en = models.CharField(max_length=512, blank=True, null=True)
    discipline = models.CharField(max_length=512, blank=True, null=True)
    email = models.CharField(max_length=512, blank=True, null=True)
    homepage = models.CharField(max_length=512, blank=True, null=True)
    phone = models.CharField(max_length=512, blank=True, null=True)
    inst = models.CharField(max_length=512, blank=True, null=True)
    inst_en = models.CharField(max_length=512, blank=True, null=True)
    instshort = models.CharField(max_length=512, blank=True, null=True)
    instshort_en = models.CharField(max_length=512, blank=True, null=True)
    fac = models.CharField(max_length=512, blank=True, null=True)
    fac_en = models.CharField(max_length=512, blank=True, null=True)
    facshort = models.CharField(max_length=512, blank=True, null=True)
    facshort_en = models.CharField(max_length=512, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    graduation_date = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'members'


# Модель связка - группа - пользователь
class Groupmembers(models.Model):
    group = models.ForeignKey('Groups', models.DO_NOTHING, primary_key=True)
    user = models.ForeignKey('Logins', models.DO_NOTHING)
    rights = models.CharField(max_length=512, blank=True, null=True)

    class Meta:
        db_table = 'groupmembers'
        unique_together = (('group', 'user'),)


# Модель для групп пользователей
class Groups(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(unique=True, max_length=128)
    description = models.CharField(max_length=512, blank=True, null=True)
    created_by = models.ForeignKey('Logins', models.DO_NOTHING, db_column='created_by')
    create_time = models.DateTimeField()
    last_change_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'groups'