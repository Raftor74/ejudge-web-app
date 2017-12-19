from __future__ import unicode_literals
from django.db import models


class Logins(models.Model):
    user_id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=64)
    email = models.CharField(max_length=128, blank=True, null=True)
    pwdmethod = models.IntegerField(default=0)
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

    class Meta:
        db_table = 'logins'

