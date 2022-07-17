from django.contrib import admin
from .models import Song, Album

# Register your models here.
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['title','arties','genre','rating','song_count']
    list_filter = ["rating",'genre']
    search_fields = ['title','arties','genre']
    list_per_page = 10
    actions = ['duplicate']

    def song_count(self, album):
        return album.song_set.count() #here reverse linking works (album.song_set), because album song_set in a queryset of songs hence it first take song and as have more than one song it append set,
    def duplicate(self, request, queryset):
        for album in queryset:
            new_album = Album()
            new_album.title = album.title+" (copy)"
            new_album.arties = album.arties
            new_album.genre = album.genre
            new_album.rating = album.rating
            new_album.save()


class SongAdmin(admin.ModelAdmin):
    list_display = ['name','lang']
    list_filter = ['lang']
    search_fields = ['name','lang']
    list_per_page = 10



admin.site.register(Album,AlbumAdmin)
admin.site.register(Song, SongAdmin)

# Register your models here.
# admin.site.register(Playlist)
# admin.site.register(Favourite)