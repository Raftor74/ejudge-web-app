from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static
from mysite import settings

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('users.urls')),
    url(r'^contests/', include('contests.urls')),
    url(r'^problems/', include('problems.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'', include('blog.urls')),
] \
              + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
              + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
