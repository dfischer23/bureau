from __future__ import unicode_literals

from people.models import Contact

from django.db import models
from django.utils.translation import ugettext as _

from django import forms
from multiselectfield import MultiSelectField
import datetime

class Room(models.Model):
    class Meta:
        verbose_name = _("Room")
        verbose_name_plural = _("Rooms")

    name = models.CharField(_("Name"), max_length=200)

    def __str__(self):
        return self.name;


class Event(models.Model):
    class Meta:
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
        ordering = ("start",)

    title = models.CharField(_("Title"), max_length=200)
    start = models.TimeField(_("Start Time"))
    end = models.TimeField(_("End Time"))

    teammember = models.ForeignKey(Contact, verbose_name=_('Team Member'), limit_choices_to={'is_teammember': True},
                               blank=True, null=True, on_delete=models.SET_NULL)
    room = models.ForeignKey(Room, verbose_name=_('Room'), blank=True, null=True, on_delete=models.SET_NULL)

    WEEKDAYS = (
    		('mon', _('Monday')),
    		('tue', _('Tuesday')),
    		('wed', _('Wednesday')),
    		('thu', _('Thursday')),
    		('fri', _('Friday')),
		)
    days = MultiSelectField(choices=WEEKDAYS, verbose_name=_('Weekdays'), max_length=20, blank=True)

    exception_until = models.DateField(_("Exception until"), blank=True, null=True)
    exception = models.CharField(_("Exception"), blank=True, max_length=200)

    def exception_if_valid(self,date):
        if self.exception_until == None or date > self.exception_until:
            return "";
        return self.exception;

    def __str__(self):
        return self.title;

