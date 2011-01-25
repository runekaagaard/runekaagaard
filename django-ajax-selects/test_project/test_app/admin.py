from django.contrib import admin
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectLookup
import ajax_select
from models import Musician, Album, Song, Mood
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

# Mood
class MoodAdmin(BaseAdmin): pass
class SongMoodLookup(AjaxSelectLookup):
    model = Song
    field_name = 'mood'
    related_model = Mood
    related_search_fields = ('mood', 'description')
    
# Album.
class AlbumAdmin(BaseAdmin): inlines = [SongInline]

# Musician.
class MusicianAdmin(BaseAdmin): pass
class MusicianLookup(AjaxSelectLookup):
    model = Album
    field_name = 'musician'
    related_model = Musician
    related_search_fields = ('first_name', 'last_name')
    
    def render_selected(self, obj): return u"%s - %s" % (obj, obj.instrument)
    
# Register.
ajax_select.register(SongMoodLookup, SongAdmin, [SongInline])
ajax_select.register(MusicianLookup, AlbumAdmin)

admin.site.register(Musician, MusicianAdmin)
admin.site.register(Mood, MoodAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(Album, AlbumAdmin)

