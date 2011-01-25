"""JQuery-Ajax Autocomplete fields for Django Forms"""
__version__ = "1.1.4"
__author__ = "crucialfelix"
__contact__ = "crucialfelix@gmail.com"
__homepage__ = "http://code.google.com/p/django-ajax-selects/"

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models.fields.related import ForeignKey, ManyToManyField
from django.forms.models import ModelForm
from django.utils.text import capfirst
from django.utils.translation import ugettext_lazy as _, ugettext

def register(lookup, admin=None, inlines=None):
    """
    Register a ajax_select lookup class.
    
    Args:
        lookup: The ajax select lookup class. Should overwrite:
            model: The model where the ajax field resides
            field_name: Name of the ajax field.
            related_model: The model the ajax field holds a relation to.
            related_search_fields: Iterable with fields that should be searched
                in when the user types in the search box.
                
        admin (optional): A given model admin class which form field will be
            converted to an ajax select type.
    """
    def get_channel_name(lookup):
        """Makes sure channel names are unique."""
        channel_name = lookup.__name__.lower()
        if channel_name in register.channels:
            i = 0
            while "channel_name_%d" %i in register.channels:
                i += 1
            channel_name =  "channel_name_%d" %i
        return channel_name
    
    channel_name = get_channel_name(lookup)
    channel = (lookup.__module__, lookup.__name__)
    register.channels[channel_name] = channel
    if admin is not None:
        admin.form = ajaxify_form(lookup, channel_name)
        #if 'inlines' in lookup:
        for inline in lookup.inlines:
            inline.form = admin.form
register.channels = {}

def get_lookup(channel_name):
    """Returns an instance of the lookup class for a given channel."""
    lookup_label = register.channels[channel_name]
    lookup_module = __import__(lookup_label[0],{},{},[''])
    lookup_class = getattr(lookup_module,lookup_label[1] )
    return lookup_class()

def ajaxify_form(lookup, channel_name):
    """Returns a ajax select form where fields have been ajaxyfied."""
    class AjaxForm(ModelForm):
        class Meta: Model = None
        setattr(Meta, 'model', lookup.model)
        
    def ajaxify_field(model, model_fieldname, channel_name, **kwargs):
        """Returns a Ajaxyfied form field."""
        from ajax_select.fields import (AutoCompleteField,
                                       AutoCompleteSelectMultipleField,
                                       AutoCompleteSelectField)
        field = model._meta.get_field(model_fieldname)
        if 'label' not in kwargs:
            kwargs['label'] = _(capfirst(unicode(field.verbose_name)))
        if 'help_text' not in kwargs:
            if isinstance(field.help_text,basestring):
                kwargs['help_text'] = _(field.help_text)
            else:
                kwargs['help_text'] = field.help_text
        if 'required' not in kwargs:
            kwargs['required'] = not field.blank
            
        if isinstance(field, ManyToManyField):
            return AutoCompleteSelectMultipleField(channel_name, **kwargs)
        elif isinstance(field, ForeignKey):
            return AutoCompleteSelectField(channel_name, **kwargs)
        else:
            return AutoCompleteField(channel_name, **kwargs)
        
    f = ajaxify_field(lookup.model,lookup.field_name, channel_name)
    AjaxForm.declared_fields[lookup.field_name] = f
    setattr(AjaxForm,lookup.field_name, f)
    return AjaxForm