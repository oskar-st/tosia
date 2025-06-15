from django.shortcuts import render
from django.utils import translation

def home(request):
    current_lang = translation.get_language()
    print("Current session lang:", current_lang)
    return render(request, 'main/home.html', {
        'current_lang': current_lang
    })