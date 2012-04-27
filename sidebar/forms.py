from django import forms
from django.utils.translation import ugettext_lazy as _

class WidgetTitleForm(forms.Form):
    """A simple form for widget title"""
    
    widget_title = forms.CharField(label=_('Title'), max_length=50)

class DefaultAdminForm(forms.Form):
    """
    A default admin form, in case widget doesn't have admin form.
    because admin form is required (to simplify validation process) in widget update. 
    this form will be used, and validated and always be valid, since we do
    nothing here.
    """
    pass
