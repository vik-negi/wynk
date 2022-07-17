# models.py is blueprint for our database, database primerialy use for user authentication and management
# its stablished a connection between database and python

# It's M of MVT use to store your data It's alo help to communicate with database
from asyncio.windows_events import NULL
from django.contrib.auth.models import User
from email.policy import default
from tkinter import CASCADE
from django.db import models

# Create your models here.

class Artist(models.Model):
    name : models.CharField(max_length=200)
    

class Album(models.Model):
    title = models.CharField(max_length=200)
    arties = models.CharField(max_length=200)
    genre = models.CharField(max_length=200,choices={
        ('Rock','Rock'),
        ('Pop Music','Pop Music'),
        ("Hip Hop Music", 'Hip Hop Music'),
        ("Hip Hop and Rap", 'Hip Hop and Rap'),
        ('Folk','Folk'),
        ('Classical','Classical'),
        ('Techno','Techno'),
        ('Country','Country'),
        ('Hollywood','Hollywood'),
        ('Bollywood','Bollywood'),
        ('K-POP','K-POP'),
        ('Metal',"Metal"),
    })
    rating = models.FloatField(default=0)

    def __str__(self):
        return (str(self.id)+" - "+self.title + "-"+self.arties+"-"+self.genre+"-"+str(self.rating))
    cover_image = models.ImageField(default=None , null=True)



class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length = 200)
    lang = models.CharField(max_length=200, choices={
        ("Hindi", "Hindi"),
        ("English", "English"),
        ("Punjabi", "Punjabi"),
        ("Kumaoni","Kumaoni"),
        ("korean","korean")
    })
    file = models.FileField(default=None, null=True)
    # arties = models.CharField(max_length=200)
    cover_image = models.ImageField(default='\static\img\diwali-india.jpg', null = True)

    @property
    def cover_image_url(self):
        if self.cover_image and hasattr(self.cover_image, 'url'):
            return self.cover_image.url
        else:
            return '\static\img\diwali-india.jpg'

    def __str__(self):
        return (str(self.id)+" - "+self.name+" "+'('+self.lang+')')

class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlistName = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    isFav = models.BooleanField(default=False)

class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

'''
Step 1. python code : model.py 
    
Step 2. python manage.py makemigration
    migrations/0001_initial.py ->intermidiate file
Step 3. run command python manage.py migrate
    This wil convert our pyhton code in migrations folder to SQL code
'''
