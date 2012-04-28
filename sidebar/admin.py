from django.contrib import admin
from sidebar.models import Sidebar
from django import forms
from django.db import models

class SidebarAdmin(admin.ModelAdmin):
    fields = ('position',)

admin.site.register(Sidebar, SidebarAdmin)

