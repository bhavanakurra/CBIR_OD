from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from detection import views
urlpatterns = [
    path('home/', views.home, name='home'),
    path('upload/',views.upload,name='upload'),
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
   urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


#127.0.0.1:8000/catalog/
