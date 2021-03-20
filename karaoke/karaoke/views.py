from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .forms import RegistrationForm, SearchForm

def index(request):
    return render(request, 'index.html')

def recording(request):
    return render(request, 'recording.html')

def songselection(request):
    keywords = ''
    form = SearchForm(request.POST or None)
    if form.is_valid():
        keywords = form.cleaned_data.get('keywords')
    else:
        form = SearchForm()
    if request.method == 'POST' and 'run_script' in request.POST:
        from .templatetags.spotify import get_search

        #clearing existing messages
        msg = messages.get_messages(request)
        for m in msg:
            pass

        #calling the search function
        st = get_search(request, keywords)
        messages.info(request, st)
        return redirect('songselection')
    return render(request, 'songselection.html', {'form': form})

def register(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        form = RegistrationForm()

        if request.method == 'POST':
            form = RegistrationForm(request.POST)
            if form.is_valid():
                form.save()
                username = form.cleaned_data.get('username')
                messages.success(request, 'Account was created successfully for ' + username + '!')
                return redirect('loginpage')


        context = {'form':form}
        return render(request, 'register.html', context)

def loginpage(request):
    if request.user.is_authenticated:
        return redirect(index)
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                messages.info(request, 'Username OR password is incorrect!')

        return render(request, 'login.html')

def logoutuser(request):
    logout(request)
    return redirect('index')
