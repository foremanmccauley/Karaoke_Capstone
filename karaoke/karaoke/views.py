from django.shortcuts import render

def index(request):
    return render(request, 'index.html')
def recording(request):
    return render(request, 'recording.html')
def songselection(request):
    return render(request, 'songselection.html')