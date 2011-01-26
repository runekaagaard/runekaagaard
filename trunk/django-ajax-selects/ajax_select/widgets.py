from ajax_select import get_lookup
from django import forms
from django.conf import settings
from django.core.urlresolvers import reverse
from django.forms.util import flatatt
from django.template.defaultfilters import escapejs
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

class AutoCompleteWidget(forms.TextInput):
    """Widget to select a search result and enter the result as raw text in the 
    text input field. The user may also simply enter text and ignore any auto 
    complete suggestions.
    """
    channel = None
    help_text = ''
    html_id = ''

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        self.help_text = kwargs.pop('help_text', '')
        super(AutoCompleteWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        value = value or ''
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)
        context = {
            'current_name': value,
            'current_id': value,
            'help_text': self.help_text,
            'html_id': self.html_id,
            'lookup_url': reverse('ajax_lookup', args=[self.channel]),
            'name': name,
            'extra_attrs':mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-","")
        }
        templates = ('autocomplete_%s.html' % self.channel,
                     'autocomplete.html')
        return mark_safe(render_to_string(templates, context))

class AutoCompleteSelectWidget(forms.widgets.TextInput):
    """Widget to select a model."""
    add_link = None
    
    def __init__(self,
                 channel,
                 help_text='',
                 *args, **kw):
        super(forms.widgets.TextInput, self).__init__(*args, **kw)
        self.channel = channel
        self.help_text = help_text

    def render(self, name, value, attrs=None):
        value = value or ''
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)
        lookup = get_lookup(self.channel)
        if value:
            objs = lookup.get_by_ids([value])
            try:
                obj = objs[0]
            except IndexError:
                raise Exception("%s cannot find object:%s" % (lookup, value))
            current_result = mark_safe(lookup.render_selected( obj ) )
        else:
            current_result = ''
        try:
            search_help = lookup.get_search_help()
        except AttributeError:
             search_help = None
             
        context = {
                'name': name,
                'html_id' : self.html_id,
                'lookup_url': reverse('ajax_lookup',
                                      kwargs={'channel':self.channel}),
                'current_id': value,
                'current_result': current_result,
                'help_text': self.help_text,
                'extra_attrs': mark_safe(flatatt(final_attrs)),
                'func_slug': self.html_id.replace("-",""),
                'add_link' : self.add_link,
                'admin_media_prefix' : settings.ADMIN_MEDIA_PREFIX,
                'search_help': search_help,
                }
        return mark_safe(render_to_string((
             'autocompleteselect_%s.html' % self.channel, 
             'autocompleteselect.html'),context))

    def value_from_datadict(self, data, files, name):
        got = data.get(name, None)
        if got:
            return long(got)
        else:
            return None
        
class AutoCompleteSelectMultipleWidget(forms.widgets.SelectMultiple):
    """Widget to select multiple models."""
    add_link = None

    def __init__(self,
                 channel,
                 help_text='',
                 show_help_text=False,#admin will also show help. set True if used outside of admin
                 *args, **kwargs):
        super(AutoCompleteSelectMultipleWidget, self).__init__(*args, **kwargs)
        self.channel = channel
        self.help_text = help_text
        self.show_help_text = show_help_text

    def render(self, name, value, attrs=None):
        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs)
        self.html_id = final_attrs.pop('id', name)
        lookup = get_lookup(self.channel)
        current_name = "" # the text field starts empty
        # eg. value = [3002L, 1194L]
        if value:
            # |pk|pk| of current
            current_ids = "|" + "|".join( str(pk) for pk in value ) + "|" 
        else:
            current_ids = "|"

        objects = lookup.get_by_ids(value)
        # text repr of currently selected items
        current_repr_json = []
        for obj in objects:
            repr = lookup.render_selected(obj)
            current_repr_json.append( """new Array("%s",%s)""" % (
                                                        escapejs(repr),obj.pk))
        current_reprs = mark_safe("new Array(%s)" % ",".join(current_repr_json))
        if self.show_help_text:
            help_text = self.help_text
        else:
            help_text = ''

        context = {
            'name':name,
            'html_id':self.html_id,
            'lookup_url':reverse('ajax_lookup',kwargs={'channel':self.channel}),
            'current':value,
            'current_name':current_name,
            'current_ids':current_ids,
            'current_reprs':current_reprs,
            'help_text':help_text,
            'extra_attrs': mark_safe(flatatt(final_attrs)),
            'func_slug': self.html_id.replace("-",""),
            'add_link' : self.add_link,
            'admin_media_prefix' : settings.ADMIN_MEDIA_PREFIX,
        }
        return mark_safe(render_to_string(('autocompleteselectmultiple_%s.html' 
            % self.channel, 'autocompleteselectmultiple.html'), context))

    def value_from_datadict(self, data, files, name):
        # eg. u'members': [u'|229|4688|190|']
        return [long(val) for val in data.get(name,'').split('|') if val]