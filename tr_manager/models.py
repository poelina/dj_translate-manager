import os
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

def get_upload_path(instance, filename):
    return os.path.join('orders', instance.service_type, filename)

class Order(models.Model):
    SERVICE_CHOICES = [
        ('text', 'Письменный перевод'),
        ('speech', 'Устный перевод'),
        ('audio', 'Перевод аудио в текст'),
    ]

    DELIVERY_CHOICES = [
        ('digital', 'Загрузить скан на сайт'),
        ('post', 'Физическая почта / Курьер'),
        ('office', 'Лично в офисе'),
    ]

    service_type = models.CharField(max_length=30, choices=SERVICE_CHOICES, verbose_name="Тип услуги")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    language_from = models.CharField(max_length=20, verbose_name="Язык оригинала")
    language_to = models.CharField(max_length=20, verbose_name="Язык перевода")

    delivery_method = models.CharField(
        max_length=30, 
        choices=DELIVERY_CHOICES, 
        null=True, 
        blank=True, 
        verbose_name="Способ передачи оригинала"
    )
    document_file = models.FileField(
        upload_to=get_upload_path, 
        null=True, 
        blank=True, 
        verbose_name="Загруженный файл"
    )
    page_count = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10000)],
        null=True, 
        blank=True, 
        verbose_name="Количество страниц"
    )
    deadline_date = models.DateField(null=True, blank=True, verbose_name="Срок исполнения")

    event_date = models.DateTimeField(null=True, blank=True, verbose_name="Дата и время устного мероприятия")

    first_name = models.CharField(max_length=100, verbose_name="Имя")
    last_name = models.CharField(max_length=100, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Электронная почта")
    phone = models.CharField(max_length=30, verbose_name="Телефон")
    
    is_company = models.BooleanField(default=False, verbose_name="Юридическое лицо")
    company_name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Название компании")

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Заказ #{self.id} ({self.get_service_type_display()}) - {self.last_name}"
