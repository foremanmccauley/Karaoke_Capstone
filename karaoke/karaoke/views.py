from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import FileResponse
from .forms import RegistrationForm, SearchForm, MP3Form
from .models import Profile, FriendRequest, MP3, GroupRequest, MP4
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .templatetags.credentials import GENIUS_ACCESS
import requests


def index(request):
    return render(request, 'index.html')
def help(request):
    return render(request, 'help.html')

def profile(request):
    if request.user.is_authenticated:
        requestProfile = Profile.objects.get(user=request.user)
        allprofiles=Profile.objects.exclude(user=request.user)
        fr = FriendRequest.objects.filter(to_user=request.user)
        gr = GroupRequest.objects.filter(to_user=request.user)
        count = 0
        in_group = False
        for profile in requestProfile.group.all():
            count = count + 1
        if count > 0:
            in_group = True
        return render(request, 'profile.html',{'allprofiles':allprofiles, 'fr':fr, 'requestProfile':requestProfile, 'in_group':in_group, 'gr':gr})

    else:
        return redirect('index')

def send_friend_request(request, id):
    from_user=request.user
    to_user=User.objects.get(id=id)
    frequest=FriendRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    return redirect('profile')

def send_group_request(request, id):
    from_user=request.user
    to_user=User.objects.get(id=id)
    grprequest=GroupRequest.objects.get_or_create(from_user=from_user,to_user=to_user)
    return redirect('profile')

def accept_friend_request(request, id):
    frequest=FriendRequest.objects.get(id=id)
    frequest.is_active = False
    frequest.save()
    user1=User.objects.get(pk=request.user.id)
    user2=User.objects.get(pk=frequest.from_user.id)
    user1.profile.friends.add(user2.profile)
    user2.profile.friends.add(user1.profile)
    return redirect('profile')

def accept_group_request(request, id):
    grprequest=GroupRequest.objects.get(id=id)
    grprequest.is_active = False
    grprequest.save()
    user1=User.objects.get(pk=request.user.id)

    user1.profile.is_group_parent = False #they accepted a request, so they cannot be the group parent
    user1.save()

    user2=User.objects.get(pk=grprequest.from_user.id)

    user1.profile.group.add(user2.profile)
    user2.profile.group.add(user1.profile)

    for profile in user2.profile.group.all():
        if profile not in user1.profile.group.all():
            user1.profile.group.add(profile)

    return redirect('profile')

def recording(request):
    if request.user.is_authenticated:
        requestProfile = Profile.objects.get(user=request.user)
        form = MP3Form(request.POST, request.FILES)
        if request.method == 'POST' and 'run_script' in request.POST:
            if form.is_valid():
                from .templatetags.upload import upload_file
                #file = request.FILES['song']
                file = request.FILES.get('song', False)
                if file:
                    try:
                        MP3.validate_audio_file(file)
                    except ValidationError:
                        messages.error(request, 'Please upload an audio file!')
                    else:
                        newsong = MP3(song = file)
                        newsong.save()

                        #attach the mp3 to the user's profile
                        requestProfile.mp3name = newsong.song.name
                        requestProfile.save()

                        # f_name is passed in to the upload function for playback purposes
                        # upload_file (in upload.py) could be modified to add the filepath to the group database
                        # may need to later pass the user information in (for group purposes)
                        f_name = 'static/media/' + newsong.song.name
                        st = upload_file(request, f_name)
                        messages.info(request, st)
                        messages.info(request, 'File successfully uploaded!')

                #return redirect('recording')
                file2 = request.FILES.get('video', False)
                if file2:
                    try:
                        MP4.validate_video_file(file2)
                    except ValidationError:
                        messages.error(request, 'Please upload an video file!')
                    else:
                        newsong = MP4(video = file2)
                        newsong.save()

                        #attach the mp4 to the user's profile
                        requestProfile.mp4name = newsong.video.name
                        requestProfile.save()

                        f_name = 'static/media/' + newsong.video.name
                        st2 = upload_file(request, f_name)
                        messages.info(request, st2)
                        messages.info(request, 'File successfully uploaded!')

                return redirect('recording')#, {'requestProfile' : requestProfile})
        else:
            form = MP3Form()

        songdetail = request.GET.get('songdetail')
        if songdetail is None:
            songdetail = ''
        url = f"https://api.genius.com/search?q={songdetail}&access_token={GENIUS_ACCESS}"
        response = requests.get(url)
        data = response.json()

        hits = data['response']['hits']

        context = {
            'hits' : hits,
            'requestProfile' : requestProfile
        }

        context.update({'form' : form})
        return render(request, 'recording.html', context)
    else:
        return redirect('profile')

def composite(request):
    if request.method == 'POST' and 'run_script' in request.POST:
        from .templatetags.composite import comp
        requestProfile = Profile.objects.get(user=request.user)
        comp(request, requestProfile)
        response= FileResponse(open('karaoke/static/media/outputs/'+requestProfile.user.username+'.mp4', 'rb'), as_attachment=True, filename='karaokevideo.mp4')
        return response

    return render(request, 'composite.html')


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
