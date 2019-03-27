from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Q

from .models import Event
import datetime

WEEKDAYS = ["mon","tue","wed","thu","fri","sat","sun"]

def render_day(request,date):
    weekday = WEEKDAYS[date.weekday()]

    return render(request, 'day.html', 
        { 'date': date,
          'date_de': date.strftime("%d.%m.%Y"),
          'weekday': dict(Event.WEEKDAYS)[weekday],
          'events': Event.objects.all().filter(Q(days__icontains=weekday)).order_by('start')
          })


@login_required
def today(request):
    date = datetime.date.today()
    return render_day(request,date);


@login_required
def day(request,year,month,day):
    date = datetime.date(year,month,day)
    return render_day(request,date);