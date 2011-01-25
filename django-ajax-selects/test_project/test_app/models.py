from django.db import models
from django.contrib import admin

class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)
    
    def __unicode__(self): return '%s %s' % (self.first_name, self.last_name)
    
class Album(models.Model):
    musician = models.ForeignKey(Musician, help_text=None)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
    
    def __unicode__(self): return self.name

class Mood(models.Model):
    mood = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self): return self.mood

class Groove(models.Model):
    groove = models.CharField(max_length=100)
    description = models.TextField()
    
    def __unicode__(self): return self.groove
    
class Song(models.Model):
    album = models.ForeignKey(Album)
    title = models.CharField(max_length=100)
    mood = models.ForeignKey(Mood, help_text=None)
    groove = models.ForeignKey(Groove, help_text=None)
    
    def __unicode__(self): return self.title