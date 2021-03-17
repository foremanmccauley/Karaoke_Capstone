from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from .forms import RegistrationForm

def index(request):
    return render(request, 'index.html')

def recording(request):
    return render(request, 'recording.html')

def songselection(request):
    return render(request, 'songselection.html')

def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()


    context = {'form':form}
    return render(request, 'register.html', context)

def login(request):
    return render(request, 'login.html')
