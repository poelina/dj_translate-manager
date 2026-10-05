from django.contrib import admin
from .models import Order

# admin1
# st_account@mail.ru
# Qwerty!@

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = ('id', 'service_type', 'last_name', 'first_name', 'email', 'created_at', 'deadline_date')
    
    list_filter = ('service_type', 'delivery_method', 'created_at')
    
    search_fields = ('last_name', 'first_name', 'email', 'phone', 'company_name')
    
    ordering = ('-created_at',)
    
    fieldsets = (
        ('Системная информация', {
            'fields': ('service_type',)
        }),
        ('Маршрут перевода', {
            'fields': ('language_from', 'language_to')
        }),
        ('Логистика и Сроки', {
            'fields': ('delivery_method', 'document_file', 'page_count', 'deadline_date', 'event_date')
        }),
        ('Данные клиента', {
            'fields': ('first_name', 'last_name', 'email', 'phone', 'is_company', 'company_name')
        }),
    )