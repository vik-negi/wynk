# purpose of views to manuplute your data and perform some operation on data it's V of "MVT"

from atexit import register
from unicodedata import name
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from Music.serializer import AlbumListSerializer
from .models import Album , Song
from Music.forms import subscriberForm
from PIL.Image import Image
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files import File
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render, redirect


# Create your views here.
def home(request):
    album_list = Album.objects.all()

    hindiSongs = Song.objects.filter(lang='Hindi')
    return render(request, 'Music/home.html', context={"album_list": album_list, "hindiSongs": hindiSongs})

def music_list(request):
    topic = "Here are the list of Music"
    music = ['Music-1', 'Music-2','Music-3','Music-4','Music-5']
    show = ""
    show+='<b>'+topic+'</b>'+'<hr>'
    for i in music:
        show+=i+'<br>'
    return HttpResponse(show)

def album_list(request):
    album_list = Album.objects.all()
    # show=""
    # for album in album_list:
    #     show+=str(album) +'<br>'
    # return HttpResponse("<h1>This is our Album list</h1><br>"+show)

    # context -->> what data you want ot show in your website

    return render(request, "Music/home.html", context={"album_list": album_list, "num_album":len(album_list)})


def album_details(request, album_id):
    album = Album.objects.filter(id=album_id).get()
    album = get_object_or_404(Album, id=album_id)
    song_list = Song.objects.filter(album=album)
    return render(request, "Music/album_details.html",context={"album":album,"song_list": song_list})

def song_list(request):
    song_list = Song.objects.all()
    show=""
    for song in song_list:
        show+=str(song)+'<br>'
    return HttpResponse('<h1>This is Our Song list</h1><br>'+show)


def subform(request):
    subscriber = subscriberForm()
    return render(request, 'Music/register.html',{ 'form': subscriber})


def hindiSongs(request):
    hindiSongs = Song.objects.filter(language='Hindi')
    #Last played song
    # last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    # if last_played_list:
    #     last_played_id = last_played_list[0]['song_id']
    #     last_played_song = Song.objects.get(id=last_played_id)
    # else:
    #     last_played_song = Song.objects.get(id=7)

    query = request.GET.get('q')

    if query:
        hindiSongs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'hindiSongs': hindiSongs}
        return render(request, 'Music/hindiSongs.html', context)

    # context = {'hindiSongs':hindiSongs,'last_played':last_played_song}
    context = {'hindiSongs':hindiSongs}
    return render(request, 'Music/hindi.html',context=context)


def englishSongs(request):

    englishSongs = Song.objects.filter(language='English')

    #Last played song
    # last_played_list = list(Recent.objects.values('song_id').order_by('-id'))
    # if last_played_list:
    #     last_played_id = last_played_list[0]['song_id']
    #     last_played_song = Song.objects.get(id=last_played_id)
    # else:
    #     last_played_song = Song.objects.get(id=7)
    #     last_played_song = None
    query = request.GET.get('q')

    if query:
        englishSongs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'englishSongs': englishSongs}
        return render(request, 'Music/englishSongs.html', context)

    # context = {'englishSongs':englishSongs,'last_played':last_played_song}
    context = {'englishSongs':englishSongs}

    return render(request, 'Music/english.html',context=context)
    # return HttpResponse("<h2>hello</h2>", englishSongs[0].name)


class AlbumList(APIView):

	def get(self, request, user_id):
		album_list = Album.objects.filter(user=User.objects.filter(id=user_id).get()).all()
		serialized_albums = AlbumListSerializer(album_list, many=True)
		return Response({"Albums": serialized_albums.data})

	def post(self, request):
		return Response({"message": "NO ACTION ON POST METHOD"})

	def patch(self, user_id):
		pass

	def put(self, user_id):
		pass


@login_required
def add_album(request):
	if request.method == "GET":
		return render(request, "Music/add_album.html")
	if request.method == "POST":
		user = request.user
		name = request.POST['album_name']
		artist = request.POST['album_artist']
		genre = request.POST['album_genre']
		rating = request.POST['album_rating']
		image = File(request.FILES.get('album_cover'))

		new_album = Album()
		new_album.user = user
		new_album.title = name
		new_album.artist = artist
		new_album.genre = genre
		new_album.rating = rating
		new_album.cover_image = image
		new_album.save()

		return redirect('album_list')

class AlbumAdd(APIView):

	def get(self, request):
		return Response({"message": "NO ACTION ON GET METHOD"})

	def post(self, request):
		user_id = request.POST['user']
		name = request.POST['album_name']
		artist = request.POST['album_artist']
		genre = request.POST['album_genre']
		rating = request.POST['album_rating']
		image = File(request.FILES.get('album_cover'))

		new_album = Album()
		new_album.user = User.objects.filter(id=user_id).get()
		new_album.title = name
		new_album.artist = artist
		new_album.genre = genre
		new_album.rating = rating
		new_album.cover_image = image
		new_album.save()

		return Response({"message": "ALBUM ADDED"})



@login_required
def add_song(request, album_id):
	if request.method == "GET":
		album = get_object_or_404(Album, id=album_id, user=request.user)
		return render(request, "Music/add_song.html", context={'album': album})
	if request.method == "POST":
		album = get_object_or_404(Album, id=album_id)
		name = request.POST['song_name']
		file = request.FILES.get('song_file')

		new_song = Song()
		new_song.album = album
		new_song.name = name
		new_song.file = file
		new_song.save()

		return redirect('album_details', album.id)


@login_required
def album_delete(request, album_id):
	album = get_object_or_404(Album, id=album_id, user=request.user)
	album.delete()
	return redirect('album_list')


@login_required
def song_delete(request, album_id, song_id):
	song = get_object_or_404(Song, id=song_id, album=album_id)
	song.delete()
	return redirect('album_details', album_id)



# how to make our own filter fro templates

# from django import template
# register = template.Library()

# @register.song_count
# def song_count(album=None):
#     return album.song_set.count()