from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
urlpatterns = [
    path('', views.home, name= 'homepage'),
    path('sort_by_category/<int:id>', views.home, name= 'sort_by_cat'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
