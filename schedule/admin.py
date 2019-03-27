from django.contrib import admin
from django import urls
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from .models import *
from django import forms

from datetime import date

from django.utils.encoding import force_text
from django.db.models import F, ExpressionWrapper, IntegerField

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib import messages

from django.contrib.admin import SimpleListFilter
from schedule.models import Event
from django.db.models import Q

class WeekdayFilter(SimpleListFilter):
    title = _('Weekday')
    parameter_name = 'days'

    def lookups(self, request, model_admin):
        return Event.WEEKDAYS

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(Q(days__icontains=self.value()))


class EventAdmin(admin.ModelAdmin):
    model = Event
    list_display = ("start","end","title","teammember","room","days","exception","exception_until")
    list_filter = ("teammember","room",WeekdayFilter)

admin.site.register(Event, EventAdmin)

class RoomAdmin(admin.ModelAdmin):
    model = Room

admin.site.register(Room, RoomAdmin)
