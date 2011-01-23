from django.db import models
from django.contrib import admin
from ajax_select import make_ajax_form

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