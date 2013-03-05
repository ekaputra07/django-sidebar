More on creating sidebar widget
===============================

Here are our simple sidebar widget, ::

    # === STEP 1 ===
    from sidebar.base import SidebarWidget, sidebar_widget
    from django import forms

    # === STEP 2 ===
    TEMPLATE = """
    {{widget_title}}
    <div class="side_block">
    <img src="{{image}}"/>
    {{text|safe}}
    </div>
    """
    
    # === STEP 3 ===
    class PromotionalForm(forms.Form):
        image = forms.CharField()
        text = forms.CharField(widget=forms.Textarea)
    
    # === STEP 4 ===
    class PromotionalImage(SidebarWidget):
        admin_form = PromotionalForm
        template_text = TEMPLATE
    
    # === STEP 5 ===
    sidebar_widget = PromotionalImage('Promotional Image','Display a promotional image with text')
    
I will break down the above code into 5 parts so we could understand more closely on how it works.

STEP 1
------
We imported **SidebarWidget** base class since every widget created must be based on this class.

Also imported **sidebar_widget**, this is just an empty variable but will be used to hold an instance of our widget object.

And we also need to import django form, since widget mostly need inputs in the admin area, which will be based on django form.
    
STEP 2
------
Widget template is a template that will be rendered to web page and filled with context/data specified in admin area.

Sidebar widget have two kinds of template that can be used:
    
The **First** is *text template*, this template mostly will be declared in the same file as the widget code itself.
    
The **Second** is *file template*, this template is a normal django template file, we can put it in our project template directory. 
    
STEP 3
------
Create a data form, this form will be displayed in admin area which you can enter data.
    
Whatever field that you create, will be available as a context data in the template. The name of the context is same as the field name.
    
Beside all available contexts based on form fields, sidebar template also have one additional context called **widget_title**, this context will hold the widget title you set in the admin area.

STEP 4
------
This is our widget class which must extends the **SidebarWidget** class, available class attributes:

* **admin_form**, (Optional) accept form class that you created in STEP 3.
* **template_text** or **template_file**, if you use template file, please provide it with the correct template file name.
    
STEP 5
------
he last step is to initialize our widget class, and assign it to *sidebar_widget* variable.
    
When initializing our widget class, **it accept two parameters**, the first one is the **name of the widget**. And the second one is the **description of the widget**.

These two information will be displayed in widget admin of Django-sidebar.