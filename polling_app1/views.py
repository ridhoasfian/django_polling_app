from django.shortcuts import render
from polling.models import Poll

def home(request):
    poll = Poll.objects.all()
    return render(request, 'home.html', {'poll':poll})
