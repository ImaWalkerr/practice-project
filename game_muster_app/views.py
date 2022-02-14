from django.shortcuts import render, redirect
from django.views.generic import ListView


from django.db import models


def main_page(request):
    return render(request, 'main_page.html')


def games_detail_page(request):
    return render(request, 'games_detail_page.html')


