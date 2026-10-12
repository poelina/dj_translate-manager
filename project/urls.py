from django.contrib import admin
from django.urls import path, include
from tr_manager import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.main, name='main'),
    path('text/', views.text, name='text'),
    path('speech/', views.speech, name='speech'),
    path('success/', views.order_success, name='order_success'),
]