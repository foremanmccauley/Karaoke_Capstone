import requests
from django import template
from django.utils.safestring import mark_safe
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, clips_array

register = template.Library()

@register.simple_tag

def Largest_Prime_Factor(n):
    prime_factor = 1
    i = 2

    while i <= n / i:
        if n % i == 0:
            prime_factor = i
            n /= i
        else:
            i += 1

    if prime_factor < n:
        prime_factor = n

    return prime_factor

def comp(request):
    mp3 = AudioFileClip('karaoke/static/media/rr.mp3')
    flist = ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

    arr = []
    cols = 2
    temp = []

    #creating clip_array
    for i in range(0,len(flist)):
        if i % cols == 0 and i != 0:
            arr.append(temp)
            temp = []
        temp.append(VideoFileClip(flist[i]))
    arr.append(temp)

    final = clips_array(arr)
    audio = CompositeAudioClip([mp3, final.audio])

    ret = final.write_videofile("test.mp4", audio=audio)
    return(final)