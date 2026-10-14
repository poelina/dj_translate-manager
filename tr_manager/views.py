import logging
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order
from django.core.exceptions import ValidationError

logger = logging.getLogger('tr_manager')

def main(request):

    return render(request, 'main.html')

def text(request):

    if request.method == 'POST':
        lang_from = request.POST.get('language_from')
        lang_to = request.POST.get('language_to')
        delivery = request.POST.get('delivery_method')
        pages = request.POST.get('page_count')
        deadline = request.POST.get('deadline_date')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        is_company = request.POST.get('is_company') == 'on'
        company_name = request.POST.get('company_name') if is_company else None

        uploaded_file = request.FILES.get('document_file')

        logger.debug(f"Payload received - User: {email}, Route: {lang_from}->{lang_to}, Method: {delivery}")

        if not all([lang_from, lang_to, first_name, last_name, email, phone]):
            logger.warning(f"Form validation aborted. Missing required fields for user: {email}")
            messages.error(request, "Пожалуйста, заполните все обязательные поля формы.")
            return render(request, 'text.html')

        try:
            clean_pages = int(pages) if pages else 1
            if clean_pages < 1:
                clean_pages = 1
        except ValueError:
            clean_pages = 1

        base_rate_per_page = 450.00
        calculated_total_price = clean_pages * base_rate_per_page

        try:
            order = Order.objects.create(
                service_type='text',
                status='new',
                price_estimate=calculated_total_price,
                language_from=lang_from,
                language_to=lang_to,
                delivery_method=delivery,
                page_count=pages if pages else 1,
                deadline_date=deadline if deadline else None,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                is_company=is_company,
                company_name=company_name,
                document_file=uploaded_file
            )

            logger.info(f"SUCCESS: Written order #{order.id} saved with computed quote value {calculated_total_price} RUB. Service: text | Client: {last_name} ({email})")
            
            request.session['latest_order_id'] = order.id
            messages.success(request, "Ваш заказ успешно принят в обработку!")
            return redirect('order_success')

        except ValidationError as val_err:
            messages.error(request, f"Ошибка валидации файла: {val_err.message}")
            return render(request, 'text.html')

        except Exception as e:
            logger.exception(f"DATABASE TRANSACTION FAILED for order request by user {email}. Error: {e}")
            messages.error(request, f"Произошла непредвиденная ошибка системы базы данных: {e}")

    return render(request, 'text.html')

def speech(request):

    if request.method == 'POST':
        lang_from = request.POST.get('language_from')
        lang_to = request.POST.get('language_to')
        speech_type = request.POST.get('speech_type')
        meet_type = request.POST.get('meet_type')
        type_online = request.POST.get('type_online')
        offline_address = request.POST.get('offline_address')
        deadline = request.POST.get('deadline_date')
        
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        
        is_company = request.POST.get('is_company') == 'on'
        company_name = request.POST.get('company_name') if is_company else None

        logger.debug(f"Inbound speech form payload received from boundary for user: {email}")

        if not all([lang_from, lang_to, speech_type, meet_type, deadline, first_name, last_name, email, phone]):
            logger.warning(f"Speech order validation rejected. Missing mandatory configuration options for user: {email}")
            messages.error(request, "Пожалуйста, заполните все обязательные разделы формы устного перевода.")
            return render(request, 'speech.html')

        try:
            order = Order.objects.create(
                service_type='speech',
                language_from=lang_from,
                language_to=lang_to,
                speech_type=speech_type,
                meeting_format=meet_type,
                online_details=type_online if meet_type == 'online-vid' else None,
                address_details=offline_address if meet_type == 'offline' else None,
                event_date=deadline if deadline else None,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                is_company=is_company,
                company_name=company_name
            )

            logger.info(f"SUCCESS: Speech translation order #{order.id} committed into database layout for client {email}")
            
            request.session['latest_order_id'] = order.id
            messages.success(request, "Ваш заказ успешно принят в обработку!")
            return redirect('order_success')

        except Exception as e:
            logger.exception(f"DATABASE TRANSACTION FAILED for order request by user {email}. Error: {e}")
            messages.error(request, f"Произошла непредвиденная ошибка системы базы данных: {e}")
        
    return render(request, 'speech.html')

def order_success(request):
    order_id = request.session.get('latest_order_id', None)
    context = {'order_id': order_id}
    return render(request, 'success.html', context)
