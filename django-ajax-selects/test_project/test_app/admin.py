from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
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
    
from django.db.models import Q

class MusicianLookup(object):

    def get_query(self,q,request):
        """ return a query set.  you also have access to request.user if needed """
        return Musician.objects.filter(Q(first_name__icontains=q))

    def format_result(self, obj):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return unicode(obj)

    def format_item(self, obj):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return unicode(obj)

    def get_objects(self, ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return Musician.objects.filter(pk__in=ids)

def register(model, channel):
    meta = str(model._meta)
    parts = meta.split(".")
    channel_name = str(channel.__name__)
    settings.AJAX_LOOKUP_CHANNELS[parts[1]] = (
        'test_app.admin', channel_name)
    
print settings.AJAX_LOOKUP_CHANNELS
class AlbumAdmin(BaseAdmin):
    form = make_ajax_form(Album, dict(musician='musician'))

register(Musician, MusicianLookup)

admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)