from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('list/', views.music_list, name="music_list"),
    path('albums/', views.album_list, name="album_list"),
    path('albums/<int:album_id>/', views.album_details, name="album_details"),
    path('song/', views.song_list, name="song_list"),
    path('register', views.subform,name="register"),
    path('album/add', views.add_album, name="add_album"),
    path('album/<int:album_id>/song/add', views.add_song, name="add_song"),
    path('album/<int:album_id>/delete', views.album_delete, name="album_delete"),
    path('album/<int:album_id>/song/<int:song_id>/delete', views.song_delete, name="song_delete"),
    path('albums/api/<int:user_id>', views.AlbumList.as_view()),
    path('album/add/api', views.AlbumAdd.as_view()),

]