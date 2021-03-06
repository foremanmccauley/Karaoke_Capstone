import requests
from django import template
from django.utils.safestring import mark_safe
from django.http import FileResponse
from django.http import HttpResponse
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, clips_array
from moviepy.audio.fx.volumex import volumex
from numpy import ceil, sqrt
from karaoke.models import Profile
from mutagen.mp3 import MP3
from wsgiref.util import FileWrapper
import subprocess
from subprocess import call
import urllib.request
import shutil



register = template.Library()

@register.simple_tag

def calc_cols(n):
    #ceiling of the sqrt of the number of videos
    num = {
        1: 1,
        2: 2,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
        8: 3,
        9: 3,
        10: 5
    }
    return num.get(n)

#def comp(request):
   # mp3 = AudioFileClip('karaoke/static/media/testfiles/rr.mp3')
   # flist = ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

#test clip arrays
# space: ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

def comp(request, requestProfile):#mp3=AudioFileClip('karaoke/static/media/testfiles/rr.mp3'), flist=['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov']):
    mp3Len = 0
    if requestProfile.mp3name:
        mp3_name = 'karaoke/static/media/' + requestProfile.mp3name
        mp3Info = MP3(mp3_name).info
        mp3Len = int(mp3Info.length)
        mp3 = AudioFileClip(mp3_name)
        mp3 = mp3.set_duration(mp3Len)
        mp3 = mp3.set_start(0.33)
    flist = []
    nlist = []
    for profile in requestProfile.group.all():
        flist.append('karaoke/static/media/' + profile.mp4name)
        nlist.append(profile.user.username)
    arr = []
    temp = []
    cols = calc_cols(len(flist))

    blank = 'karaoke/static/media/blank.mp4'
    #adding a blank file if there's an uneven number of videos
    if len(flist) == 3 or len(flist) == 5 or len(flist) == 7:
        flist.append(blank)
        nlist.append('blank.mp4')

    #creating clip_array
    for i in range(0,len(flist)):
        convName = ''
        if nlist[i] != 'blank.mp4':
            convName = 'karaoke/static/media/converted/' + nlist[i] + '.mp4'
        else:
            convName = nlist[i]
        if i % cols == 0 and i != 0:
            arr.append(temp)
            temp = []
        subprocess.call(['ffmpeg', '-i', flist[i], convName])
        tempVid = VideoFileClip(convName).margin(10).set_fps(24)
        temp.append(tempVid)
    arr.append(temp)

    final = clips_array(arr)
    mp3 = mp3.fx(volumex, 0.20)
    audio = CompositeAudioClip([mp3, final.audio])
    final = final.set_audio(audio)
    final.write_videofile("karaoke/static/media/outputs/" + requestProfile.user.username + ".mp4", codec='libx264', audio_codec='aac')
    #print("Passed 1")

    #final.write_videofile("karaoke/static/media/outputs/" + 'hello' + ".mp4", codec='libx264', audio_codec='aac')    
    #response= FileResponse(open('karaoke/static/media/outputs/'+requestProfile.user.username+'.mp4', 'rb'), as_attachment=True, filename='test.mp4')
   # print("Passed 2")
    #return (response)
    return(final)
