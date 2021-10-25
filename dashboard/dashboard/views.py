from django.views.generic import TemplateView
from django.shortcuts import render


class HomePage(TemplateView):
    template_name = 'homepage.html'

class ThanksPage(TemplateView):
    template_name = 'thanks.html'


    