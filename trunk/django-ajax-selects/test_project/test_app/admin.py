from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from models import Musician, Album

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
    

class AlbumAdmin(BaseAdmin):
    form = make_ajax_form(Album, dict(musician='musician'))
    
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)