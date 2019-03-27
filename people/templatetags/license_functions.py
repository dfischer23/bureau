from django import template

register = template.Library()

@register.filter
def has_license(student,license):
	return student.licensegiven_set.filter(license=license).exists()

@register.filter
def license_comment(student,license):
	r = student.licensegiven_set.filter(license=license)
	if r.count() > 0:
		return r[0].comment or ""
	else:
		return ""

@register.filter
def prefix(value,prefix):
	if value == "":
		return ""
	return prefix + value
