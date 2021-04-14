import requests
from django import template
from django.utils.safestring import mark_safe
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, clips_array
from moviepy.audio.fx.volumex import volumex

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
    mp3 = AudioFileClip('karaoke/static/media/testfiles/rr.mp3')
    flist = ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

#test clip arrays
# space: ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']
# ryan: ['ryan1.mov', 'ryan2.mov']

def comp(request, uid='001', mp3=AudioFileClip('karaoke/static/media/testfiles/rr.mp3'), flist=['karaoke/static/media/testfiles/ryan1.mov', 'karaoke/static/media/testfiles/ryan2.mov']):
    arr = []
    cols = 2
    temp = []

    #creating clip_array
    for i in range(0,len(flist)):
        if i % cols == 0 and i != 0:
            arr.append(temp)
            temp = []
        temp.append(VideoFileClip(flist[i]).margin(10))
    arr.append(temp)

    final = clips_array(arr)
    mp3 = mp3.fx(volumex, 0.25)
    audio = CompositeAudioClip([mp3, final.audio])
    final = final.set_audio(audio)
    final.write_videofile("karaoke/static/media/outputs/" + uid + ".mp4", codec='libx264', audio_codec='aac')
    return(final)