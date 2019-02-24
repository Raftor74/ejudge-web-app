from __future__ import unicode_literals
from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

"""Модели для работы с курсами, темами, уроками"""


# Класс новостей
class News(models.Model):
    title = models.CharField(max_length=200)
    text = RichTextUploadingField(blank=True, default='')
    time = models.DateTimeField()

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

    def __str__(self):
        return "%s" % self.title


# Класс курсов
class Course(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name="URL")

    class Meta:
        ordering = ['id']
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return "%s" % self.name


# Класс уроков
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='courses', verbose_name="Курс")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True, verbose_name="URL")
    text = RichTextUploadingField(blank=True, default='')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['id']
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        index_together = [
            ['id', 'slug']
        ]

    def __str__(self):
        return "%s" % self.name