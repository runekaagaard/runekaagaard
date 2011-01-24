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

def register(lookup, admin=None):
    """
    Register a ajax_select lookup class.
    
    Args:
        lookup: The ajax select lookup class. Should overwrite:
            model: The model where the ajax field resides
            field_name: Name of the ajax field.
            related_model: The model the ajax field holds a relation to.
            related_search_fields: Iterable with fields that should be searched
                in, when the user types in the search box.
                
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
    register.channels[channel_name] = (lookup.__module__, lookup.__name__)
    if admin is not None:
        admin.form = make_ajax_form(lookup.model, 
                                    {lookup.field_name: channel_name})
register.channels = {}

def get_lookup(channel):
    """Returns an instance of the lookup class for a given channel."""
    lookup_label = register.channels[channel]
    lookup_module = __import__( lookup_label[0],{},{},[''])
    lookup_class = getattr(lookup_module,lookup_label[1] )
    return lookup_class()

def make_ajax_form(model,fieldlist,superclass=ModelForm):
    """ this will create a ModelForm subclass inserting
            AutoCompleteSelectMultipleField (many to many),
            AutoCompleteSelectField (foreign key)

        where specified in the fieldlist:

            dict(fieldname='channel', ...)

        usage:
            class YourModelAdmin(Admin):
                ...
                form = make_ajax_form(YourModel, dict(contacts='contact',
                                                      author='contact'))
                                                     
            where 'contacts' is a many to many field, specifying to use the 
            lookup channel 'contact' and where 'author' is a foreign key field, 
            specifying here to also use the lookup channel 'contact'

    """

    class TheForm(superclass):
        class Meta:
            pass
        setattr(Meta, 'model', model)

    for model_fieldname,channel in fieldlist.iteritems():
        f = make_ajax_field(model,model_fieldname,channel)
        TheForm.declared_fields[model_fieldname] = f
        TheForm.base_fields[model_fieldname] = f
        setattr(TheForm,model_fieldname,f)

    return TheForm


def make_ajax_field(model,model_fieldname,channel,**kwargs):
    """ makes an ajax select / multiple select / autocomplete field
        copying the label and help text from the model's db field
    
        optional args:
            help_text - note that django's ManyToMany db field will append 
                'Hold down "Control", or "Command" on a Mac, to select more than one.'
                to your db field's help text.
                Therefore you are better off passing it in here
            label - default is db field's verbose name
            required - default's to db field's (not) blank
            """

    from ajax_select.fields import (AutoCompleteField,
                                   AutoCompleteSelectMultipleField,
                                   AutoCompleteSelectField)

    field = model._meta.get_field(model_fieldname)
    if kwargs.has_key('label'):
        label = kwargs.pop('label')
    else:
        label = _(capfirst(unicode(field.verbose_name)))
    if kwargs.has_key('help_text'):
        help_text = kwargs.pop('help_text')
    else:
        if isinstance(field.help_text,basestring):
            help_text = _(field.help_text)
        else:
            help_text = field.help_text
    if kwargs.has_key('required'):
        required = kwargs.pop('required')
    else:
        required = not field.blank

    if isinstance(field,ManyToManyField):
        f = AutoCompleteSelectMultipleField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    elif isinstance(field,ForeignKey):
        f = AutoCompleteSelectField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    else:
        f = AutoCompleteField(
            channel,
            required=required,
            help_text=help_text,
            label=label,
            **kwargs
            )
    return f


