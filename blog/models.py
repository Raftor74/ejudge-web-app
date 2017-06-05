from django.db import models

# Create your models here.


class News (models.Model):
	title = models.CharField(max_length=200)
	text = models.TextField()
	time = models.DateTimeField()

	def __str__(self):
		return self.title

class Course (models.Model):
	name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
	slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name="URL")

	class Meta:
		ordering = ['id']
		verbose_name = 'Курс'
		verbose_name_plural = 'Курсы'

	def __str__(self):
		return self.name

class Lesson (models.Model):
	course = models.ForeignKey(Course, related_name='courses', verbose_name="Курс")
	name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
	slug = models.SlugField(max_length=200, db_index=True, verbose_name="URL")
	text = models.TextField(blank=True, verbose_name="Текст")
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
		return self.name