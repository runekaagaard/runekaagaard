from ajax_select.fields import autoselect_fields_check_can_add
from django.contrib import admin
from django.db.models import Q

class AjaxSelectAdmin(admin.ModelAdmin):
    
    """ in order to get + popup functions subclass this or do the same hook inside of your get_form """
    
    def get_form(self, request, obj=None, **kwargs):
        form = super(AjaxSelectAdmin,self).get_form(request,obj,**kwargs)
        autoselect_fields_check_can_add(form,self.model,request.user)
        return form

class AjaxSelectLookup(object):
    def render_dropdown_item(self, obj): return obj.__str__()
    def render_selected(self, obj): return obj.__str__()
    
    def get_by_pk(self, id, request):
        return self.related_model.objects.get(pk=id)
    
    def get_by_ids(self, ids):
        return self.related_model.objects.filter(pk__in=ids)
    
    def get_by_query(self, q, request):
        qs = Q()
        for field in self.related_search_fields:
            qs = qs | Q(**{'%s__icontains' % field: q})
        return self.related_model.objects.filter(qs)