from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from .models import Student
from django.shortcuts import render

@login_required
def index(request):
    return render(request, 'students.html', 
        {'students': Student.objects.all() })
