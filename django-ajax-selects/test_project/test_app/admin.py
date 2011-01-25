from django.contrib import admin
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectLookup
import ajax_select
from models import Musician, Album, Song, Mood, Groove
from django.conf import settings

class BaseAdmin(AjaxSelectAdmin):
    class Media:
        css = {
            "all": ("/media/css/jquery.autocomplete.css",
                    
                    )
        }
        js = ("https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js",
              "/media/js/jquery.autocomplete.js",
              "/media/js/ajax_select.js",
              )

# Song.
class SongAdmin(BaseAdmin): pass
class SongInline(admin.TabularInline): 
    model = Song
    extra = 1

# Mood
class MoodAdmin(BaseAdmin): pass
class SongMoodLookup(AjaxSelectLookup):
    model = Song
    field_name = 'mood'
    related_model = Mood
    related_search_fields = ('mood', 'description')
    inlines = [SongInline]

# Groove
class GrooveAdmin(BaseAdmin): pass
class SongGrooveLookup(AjaxSelectLookup):
    model = Song
    field_name = 'groove'
    related_model = Groove
    related_search_fields = ('groove', 'description')
    inlines = [SongInline]

# Album.
class AlbumAdmin(BaseAdmin): inlines = [SongInline]

# Musician.
class MusicianAdmin(BaseAdmin): pass
class AlbumMusicianLookup(AjaxSelectLookup):
    model = Album
    field_name = 'musician'
    related_model = Musician
    related_search_fields = ('first_name', 'last_name')
    
    def render_selected(self, obj): return u"%s - %s" % (obj, obj.instrument)
    
# Register.
ajax_select.register(SongMoodLookup, SongAdmin)
ajax_select.register(SongGrooveLookup, SongAdmin)
ajax_select.register(AlbumMusicianLookup, AlbumAdmin)

admin.site.register(Musician, MusicianAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Groove, GrooveAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)

