from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Order

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

        if not all([lang_from, lang_to, first_name, last_name, email, phone]):
            messages.error(request, "Пожалуйста, заполните все обязательные поля формы.")
            return render(request, 'text.html')

        try:
            order = Order.objects.create(
                service_type='text',
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
            
            request.session['latest_order_id'] = order.id
            messages.success(request, "Ваш заказ успешно принят в обработку!")
            return redirect('order_success')

        except Exception as e:
            messages.error(request, f"Произошла непредвиденная ошибка системы базы данных: {e}")

    return render(request, 'text.html')

def speech(request):

    if request.method == 'POST':
        pass #!
    return render(request, 'speech.html')

def audio(request):

    if request.method == 'POST':
        pass #!
    return render(request, 'audio.html')

def order_success(request):
    order_id = request.session.get('latest_order_id', None)
    context = {'order_id': order_id}
    return render(request, 'success.html', context)
