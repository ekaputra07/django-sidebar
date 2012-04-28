from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings

class Sidebar(models.Model):
    position = models.CharField(_('Sidebar Position'),
                                max_length=100,
                                unique=True,
                                choices=settings.AVAILABLE_SIDEBARS,
                                help_text=_('This is position of the sidebar.'))

    def __unicode__(self):
        for position in settings.AVAILABLE_SIDEBARS:
            if position[0] == self.position:
                return u'%s' % position[1]


    class Meta:
        verbose_name = _('Sidebar')
        verbose_name_plural = _('Sidebars')

class SidebarWidget(models.Model):
    title = models.CharField(max_length=150)
    sidebar = models.ForeignKey(Sidebar)
    widget = models.CharField(max_length=50)
    content = models.TextField(blank=True, null=True)
    order = models.IntegerField(blank=True, null=True, default=100)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ('order',)
        db_table = 'sidebar_widget'

