from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, RegisterForm


def main(request):
    return render(request, 'main.html')

def login_page(request):
    if request.method == "POST":
        user_email = request.POST.get("user_email")
        user_password = request.POST.get("password")

        # if user_email == "bob@mail.ru" and user_password == "bobisthebest":
        #     return HttpResponse("<h1>Hello me!</h1>")
        # else:
        #     return HttpResponse(f"<h1>Hello, {user_email}</h1>")
        
    else:
        user_form = UserForm()
        return render(request, "tr_manager/login_page.html", {"login_form": user_form})