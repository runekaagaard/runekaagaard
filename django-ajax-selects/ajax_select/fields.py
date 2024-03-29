from ajax_select import get_lookup
from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
from ajax_select.widgets import (AutoCompleteSelectMultipleWidget, 
                                 AutoCompleteSelectWidget, AutoCompleteWidget)

class AutoCompleteSelectFieldBase(forms.fields.CharField):
    def check_can_add(self, user, model):
        """Check if the user can add the model, deferring first to the channel if 
        it implements can_add() else using django's default perm check. If it 
        can add, then enable the widget to show the + link."""
        lookup = get_lookup(self.channel)
        try:
            can_add = lookup.can_add(user,model)
        except AttributeError:
            ctype = ContentType.objects.get_for_model(model)
            can_add = user.has_perm("%s.add_%s" % (ctype.app_label,ctype.model))
        if can_add:
            self.widget.add_link = reverse('add_popup',kwargs={
                'app_label': model._meta.app_label,
                'model':model._meta.object_name.lower()})

class AutoCompleteSelectField(AutoCompleteSelectFieldBase):
    """Form field to select a model for a ForeignKey db field."""
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        widget = kwargs.get("widget", False)
        if not widget or not isinstance(widget, AutoCompleteSelectWidget):
            kwargs["widget"] = AutoCompleteSelectWidget(
                channel=channel, 
                help_text=kwargs.get('help_text', _('Enter text to search.')))
        super(AutoCompleteSelectField, self).__init__(max_length=255,*args, 
                                                      **kwargs)

    def clean(self, value):
        if value:
            lookup = get_lookup(self.channel)
            objs = lookup.get_by_ids( [ value] )
            if len(objs) != 1:
                # someone else might have deleted it while you were editing
                # or your channel is faulty
                # out of the scope of this field to do anything more than tell 
                # you it doesn't exist
                raise forms.ValidationError(u"%s cannot find object: %s" % 
                                            (lookup,value))
            return objs[0]
        else:
            if self.required:
                raise forms.ValidationError(self.error_messages['required'])
            return None

class AutoCompleteSelectMultipleField(AutoCompleteSelectFieldBase):
    """Form field to select multiple models for a ManyToMany db field."""
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        help_text = kwargs.get('help_text',_('Enter text to search.'))
        # admin will also show help text, so by default do not show it in widget
        # if using in a normal form then set to True so the widget shows help
        show_help_text = kwargs.get('show_help_text',False)
        kwargs['widget'] = AutoCompleteSelectMultipleWidget(
            channel=channel, help_text=help_text, show_help_text=show_help_text)
        super(AutoCompleteSelectMultipleField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value and self.required:
            raise forms.ValidationError(self.error_messages['required'])
        return value # a list of IDs from widget value_from_datadict
    
class AutoCompleteField(forms.CharField):
    """Field uses an AutoCompleteWidget to lookup possible completions using a 
    channel and stores raw text (not a foreign key).
    """
    channel = None

    def __init__(self, channel, *args, **kwargs):
        self.channel = channel
        widget = AutoCompleteWidget(channel,help_text=kwargs.get('help_text', 
                                                    _('Enter text to search.')))
        defaults = {'max_length': 255,'widget': widget}
        defaults.update(kwargs)
        super(AutoCompleteField, self).__init__(*args, **defaults)