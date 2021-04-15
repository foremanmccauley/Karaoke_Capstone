import requests
from django import template
from django.utils.safestring import mark_safe
from moviepy.editor import VideoFileClip, AudioFileClip, CompositeAudioClip, clips_array
from moviepy.audio.fx.volumex import volumex
from numpy import ceil, sqrt

register = template.Library()

@register.simple_tag

def calc_cols(n):
    #ceiling of the sqrt of the number of videos
    return ceil(sqrt(n))

def comp(request):
    mp3 = AudioFileClip('karaoke/static/media/testfiles/rr.mp3')
    flist = ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

#test clip arrays
# space: ['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']

def comp(request, uid='001', mp3=AudioFileClip('karaoke/static/media/testfiles/rr.mp3'), flist=['karaoke/static/media/testfiles/1.mp4', 'karaoke/static/media/testfiles/2.mov', 'karaoke/static/media/testfiles/4.mov', 'karaoke/static/media/testfiles/5.mov']):
    arr = []
    temp = []
    cols = calc_cols(len(flist))

    #creating clip_array
    for i in range(0,len(flist)):
        if i % cols == 0 and i != 0:
            arr.append(temp)
            temp = []
        temp.append(VideoFileClip(flist[i]).margin(10))
    arr.append(temp)

    final = clips_array(arr)
    mp3 = mp3.fx(volumex, 0.20)
    audio = CompositeAudioClip([mp3, final.audio])
    final = final.set_audio(audio)
    final.write_videofile("karaoke/static/media/outputs/" + uid + ".mp4", codec='libx264', audio_codec='aac')
    return(final)