from django.contrib import admin
from django.urls import path, include
from tr_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
]