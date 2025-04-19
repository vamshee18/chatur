from django.shortcuts import render
from .models import Prompt

def home(request):
    prompts = Prompt.objects.all()
    return render(request, 'prompts/index.html', {'prompts': prompts})
