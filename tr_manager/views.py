from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import UserForm, RegisterForm


def main(request):
    return render(request, 'main.html')

def text(request):
    return render(request, 'text.html')

def speech(request):
    return render(request, 'verbal.html')

def audio(request):
    return render(request, 'audio.html')