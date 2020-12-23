from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Song
from .forms import *
from django.contrib import messages

# Create your views here.


@login_required(login_url='accounts:login')
def general(request):
    user = request.user
    songs = Song.objects.all().filter(user=user)
    if len(songs)==0:
        messages.info(request,f'Your playlist is empty.')
    return render(request, 'playlist/general.html', {'songs': songs})


def emotion(request, type):
    user = request.user
    songs = Song.objects.all().filter(user=user, type=type)
    if len(songs)==0:
        messages.info(request,f'Your playlist is empty.')
    dic = {0: 'Happy',
           1: 'Angry',
           2: 'Sad',
           3: 'Neutral'}
    return render(request, 'playlist/type.html', {'songs': songs, 'type': dic[type],'emotion':type})


@login_required(login_url='accounts:login')
def song_upload(request,type):
    if request.method == "POST":
        form = SongUploadForm(request.POST, request.FILES)
        instance = form.save(commit=False)
        instance.user = request.user
        instance.type=type
        instance.save()
        return redirect('startpage')
    else:
        form = SongUploadForm()
    return render(request, 'playlist/song_upload.html', {'form': form,'type':type})


@login_required(login_url='accounts:login')
def up_song(request):
    if request.method == "POST":
        form = SongUploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            typee=request.POST.get('playlist')
            instance.type=typee
            instance.save()
            return redirect('startpage')
    else:
        form = SongUploadForm()
    return render(request, 'playlist/up-song.html', {'form': form})


def delete(request,type,id):
    song=Song.objects.get(pk=id)
    song.delete()
    if type==4:
        return redirect('playlist:general')
    else:
        return redirect('playlist:emotion',type=type)
