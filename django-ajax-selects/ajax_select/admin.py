from ajax_select.fields import (AutoCompleteSelectField,
                                AutoCompleteSelectMultipleField)
from django.contrib import admin
from django.db.models import Q


class AjaxSelectAdmin(admin.ModelAdmin):
    """Ajax select base ModelAdmin class. Subclass this to make the plus(+)
    sign work correctly.
    """
            
    def get_form(self, request, obj=None, **kwargs):
        def check_can_add(form, model,user):
            """Check the form's fields for any autoselect fields and enable 
            their widgets with + sign add links if permissions allow."""
            for name,form_field in form.declared_fields.iteritems():
                if isinstance(form_field,(AutoCompleteSelectMultipleField, 
                                          AutoCompleteSelectField)):
                    db_field = model._meta.get_field_by_name(name)[0]
                    form_field.check_can_add(user,db_field.rel.to)
                
        form = super(AjaxSelectAdmin,self).get_form(request,obj,**kwargs)
        for inline in self.inlines:
            check_can_add(inline.form, inline.model, request.user)
        check_can_add(form, self.model, request.user)
        return form

class AjaxSelectLookup(object):
    """Default ajax select lookup class to subclass from."""
    
    inlines = []
    
    def render_dropdown_item(self, obj): return obj.__str__()
    def render_selected(self, obj): return obj.__str__()
    
    def get_by_pk(self, id, request):
        return self.related_model.objects.get(pk=id)
    
    def get_by_ids(self, ids):
        return self.related_model.objects.filter(pk__in=ids)
    
    def get_by_query(self, q, request):
        """Uses self.related_search_fields to build a queryset. This is the
        only place self.related_search_fields is used."""
        qs = Q()
        for field in self.related_search_fields:
            qs = qs | Q(**{'%s__icontains' % field: q})
        return self.related_model.objects.filter(qs)