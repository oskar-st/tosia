from django.shortcuts import render, redirect
from django.conf import settings
from django.utils import translation

# Create your views here.

def home(request):
    return render(request, 'main/home.html')

def switch_language(request):
    if request.method == 'POST':
        language = request.POST.get('language')
        if language in [lang[0] for lang in settings.LANGUAGES]:
            translation.activate(language)
            request.session['django_language'] = language
    return redirect(request.POST.get('next', '/'))
