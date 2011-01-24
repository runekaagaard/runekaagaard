from django.contrib import admin
from ajax_select import make_ajax_form
from ajax_select.admin import AjaxSelectAdmin
from models import Musician, Album
from django.conf import settings
from django.db.models import Q
from random import randint

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
    
class AjaxSelectLookup(object):
    def get_query_by_id(self, id, request):
        return self.related_model.objects.get(pk=id)
    
    def format_result(self, obj):
        """ the search results display in the dropdown menu.  may contain html and multiple-lines. will remove any |  """
        return unicode(obj)

    def format_item(self, obj):
        """ the display of a currently selected object in the area below the search box. html is OK """
        return "%s - extra" % unicode(obj)

    def get_objects(self, ids):
        """ given a list of ids, return the objects ordered as you would like them on the admin page.
            this is for displaying the currently selected items (in the case of a ManyToMany field)
        """
        return self.related_model.objects.filter(pk__in=ids)
    
    def get_query(self, q, request):
        """ return a query set. you also have access to request.user if needed """
        qs = Q()
        for field in self.related_search_fields:
            qs = qs | Q(**{'%s__icontains' % field: q})
        return self.related_model.objects.filter(qs)

def register(lookup, admin=None):
    channel_name = 'lookup_%d' % randint(0,999999)
    settings.AJAX_LOOKUP_CHANNELS[channel_name] = (lookup.__module__, 
                                                        lookup.__name__)
    if admin is not None:
        admin.form = make_ajax_form(lookup.model, 
                                    {lookup.field_name: channel_name})

class AlbumAdmin(BaseAdmin): pass

class MusicianLookup(AjaxSelectLookup):
    model = Album
    field_name = 'musician'
    related_model = Musician
    related_search_fields = ('first_name', 'last_name')
register(MusicianLookup, AlbumAdmin)
    
    
    
admin.site.register(Musician, MusicianAdmin)
admin.site.register(Album, AlbumAdmin)