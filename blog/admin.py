from django.contrib import admin

# Register your models here.
from blog.models import News, Course, Lesson

admin.site.register(News)
admin.site.register(Course)
admin.site.register(Lesson)