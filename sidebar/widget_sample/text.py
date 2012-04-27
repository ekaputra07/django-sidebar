from sidebar.base import SidebarWidget, sidebar_widget
from django import forms

"""
TEMPLATE : Can be a template file or just a short text like below.
all variable came from a admin_form value, any form field declared in
admin_form Form, will be available in template context.

Available context variable in template is:
    1. All form field by admin_form Form
    2. A widget title {{widget_title}}

An admin form is optional, but TEMPLATE must exists.
"""

TEMPLATE = """
<div class="side_block">
{{text|safe}}
</div>
"""

class TextForm(forms.Form):
    """ Just a normal django form """
    text = forms.CharField(widget=forms.Textarea)

class TextSidebarWidget(SidebarWidget):
    """ Sidebar class must a subclass of SidebarWidget class"""
    
    admin_form = TextForm
    template_text = TEMPLATE

# Here we register out Widget, New widget instance must be in sidebar_widget variable
sidebar_widget = TextSidebarWidget(
                            'Text Widget',
                            'Display custom text or Html'
                            )

