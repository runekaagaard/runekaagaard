from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin, AjaxSelectLookup
import ajax_select
from models import Musician, Album
from django.conf import settings

class BaseAdmin(AjaxSelectAdmin):
    class Media:
        css = {
            "all": ("/media/css/jquery.autocomplete.css",
                    "/media/css/iconic.css",
                    )
        }
        js = ("https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js",
              "/media/js/jquery.autocomplete.js",
              "/media/js/ajax_select.js",
              )

class MusicianAdmin(BaseAdmin): pass
class AlbumAdmin(BaseAdmin): pass

class MusicianLookup(AjaxSelectLookup):
    model = Album
    field_name = 'musician'
    related_model = Musician
    related_search_fields = ('first_name', 'last_name')
    
    def render_selected(self, obj): return u"%s - %s" % (obj, obj.instrument)

ajax_select.register(MusicianLookup, AlbumAdmin)    
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)