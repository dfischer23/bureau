from django import template
from dateutil import parser
import datetime

register = template.Library()

@register.filter
def exception_if_valid(event,date):
	return event.exception_if_valid(date)
