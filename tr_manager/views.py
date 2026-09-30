from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, RegisterForm


def main(request):
    return render(request, 'main.html')