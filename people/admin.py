from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from .models import *
from django import forms

from datetime import date

from django.utils.encoding import force_text
from django.db.models import F, ExpressionWrapper, IntegerField

# set a default filter option [https://stackoverflow.com/questions/851636/default-filter-in-django-admin]
class DefaultListFilter(admin.SimpleListFilter):
    all_value = '_all'

    def default_value(self):
        raise NotImplementedError()

    def queryset(self, request, queryset):
        if self.parameter_name in request.GET and request.GET[self.parameter_name] == self.all_value:
            return queryset

        if self.parameter_name in request.GET:
            return queryset.filter(**{self.parameter_name:request.GET[self.parameter_name]})

        return queryset.filter(**{self.parameter_name:self.default_value()})

    def choices(self, cl):
        yield {
            'selected': self.value() == self.all_value,
            'query_string': cl.get_query_string({self.parameter_name: self.all_value}, []),
            'display': _('All'),
        }
        for lookup, title in self.lookup_choices:
            yield {
                'selected': self.value() == force_text(lookup) or (self.value() == None and force_text(self.default_value()) == force_text(lookup)),
                'query_string': cl.get_query_string({
                    self.parameter_name: lookup,
                }, []),
                'display': title,
            }

class StudentStatusFilter(DefaultListFilter):
    title = _('Status ')
    parameter_name = 'status__exact'

    def lookups(self, request, model_admin):
        return Student.STATUS_CHOICES

    def default_value(self):
        return "active"



class NoteForm(forms.ModelForm):
    class Meta:
        widgets = {"content": forms.Textarea(attrs={"rows": 4, "cols":50 })}

class NoteInline(admin.TabularInline):
    extra = 0
    model = Note
    form = NoteForm
    fields = ("content",)


class StudentAdmin(admin.ModelAdmin):
    model = Student
    def get_list_display(self, request, obj=None):
        status = request.GET.get("status__exact", "active")

        if status == "active":
            return ("name", "first_name", "calc_level")
        elif status == "in_admission_procedure":
            return ("name", "first_name", "application_note")
        elif status == "intent_declared":
            return ("name", "first_name", "planned_enrollment", "application_note")
        elif status == "waitlisted":
            return ("name", "first_name", "waitlist_position", "application_note")
        elif status == "alumnus":
            return ("name", "first_name", "last_day", "application_note")

        return ("name", "first_name", "status")

    search_fields = ["first_name", "name"]
#    list_filter = ("status",)
    list_filter = (StudentStatusFilter,)
    filter_horizontal = ("guardians",)
    readonly_fields = ("guardians_links","calc_level")
    inlines = [
       NoteInline,
    ]

    def get_fieldsets(self, request, obj=None):
        fieldsets = (
                (None, {
                    "fields": ("short_name", "name", "first_name", "status", "dob", "pob", "address", "guardians_links")
                }),)

        if obj.status == "in_admission_procedure":
            fieldsets += ((_("Application"), {
                        "fields":(
                        "planned_enrollment", "application_note"
                    )}),)

        if obj.status == "intent_declared":
            fieldsets += ((_("Application"), {
                        "fields":(
                        "planned_enrollment", "application_note"
                    )}),)

        if obj.status == "waitlisted":
            fieldsets += ((_("Waitlist"), {
                        "fields":(
                        "waitlist_position", "planned_enrollment", "application_note"
                    )}),)

        fieldsets += (
                (_("Class Level"), {
                    "classes":("collapse",),
                    "fields":(
                    "first_day", "last_day",
                    "first_enrollment",
                    "level_ofs", "level_ref",
                    "calc_level"
                )}),
                (_("Formalities"), {
                    "classes":("collapse",),
                    "fields":(
                    "gender", "language",
                    "citizenship", "denomination",
                    "after_school_care", "district_school",
                    "privacy_policy_agreement", "vaccination_policy_agreement", "is_sibling"
                )}),
                (_("Edit Guardians"), {
                    "classes":("collapse",),
                    "fields": (
                    "guardians",
                )})
            )

        return fieldsets;
    	

    def guardians_links(self, obj):
        guardians = obj.guardians.all()

        links = [];
        for guardian in guardians:
        	change_url = urlresolvers.reverse("admin:people_contact_change", args=(guardian.id,))
        	links.append('<a href="%s">%s</a>' % (change_url, guardian))
        return format_html("<br>".join(links));
    guardians_links.short_description = _("Guardians")

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.name;
    get_full_name.short_description = _("Name")

    def calc_level(self, obj):
    	if not obj.level_ref or not obj.level_ofs:
    		return "N/A"
    	today = date.today();
    	current_year = today.year-1 if today.month < 8 else today.year
    	level =  current_year - (int(obj.level_ref) - int(obj.level_ofs))
    	return(level)
        #return("%i (for %i/%i)" % (level, current_year, current_year+1));
        
    calc_level.short_description = _("Class Level")

    # to order by calculated level [https://stackoverflow.com/questions/42659741/django-admin-enable-sorting-for-calculated-fields]
    calc_level.admin_order_field = 'level'
    def get_queryset(self, request):
        qs = super(StudentAdmin, self).get_queryset(request)
        qs = qs.annotate(level=ExpressionWrapper(F("level_ref")-F("level_ofs"), output_field=IntegerField())).order_by("level")
        return qs;

admin.site.register(Student, StudentAdmin)



#class ContactInline(admin.TabularInline):
#    extra = 0
#    model = Contact
#    classes = ["collapse"]

#class StudentAddressInline(admin.TabularInline):
#    extra = 0
#    model = Student
#    fields = ("name", "first_name")


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ("name","first_name","kind","phone_number","cellphone_number","email_address")
    search_fields = ["name"]
    list_filter = ("kind",)
    readonly_fields = ("student_links",)

    def get_fields(self, request, obj=None):
        if obj.is_teammember:
            return ("name", "first_name", "kind", "address", "phone_number", "cellphone_number", "email_address", "is_teammember", "team_email_address", "student_links")
        return ("name", "first_name", "kind", "address", "phone_number", "cellphone_number", "email_address", "on_address_list", "is_teammember", "student_links")

    def student_links(self, obj):
        students = obj.students.all()

        links = [];
        for student in students:
            change_url = urlresolvers.reverse("admin:people_student_change", args=(student.id,))
            links.append('<a href="%s">%s</a>' % (change_url, student))
        return format_html("<br>".join(links));
    student_links.short_description = _("Students")

admin.site.register(Contact, ContactAdmin)


class AddressAdmin(admin.ModelAdmin):
    model = Address
#    inlines = [
#    	ContactInline,
#    	StudentAddressInline
#    ]
    list_display = ("street", "city")
    readonly_fields = ("student_links","contact_links")

    def student_links(self, obj):
        students = obj.student_set.all()
        links = [];
        for student in students:
            change_url = urlresolvers.reverse("admin:people_student_change", args=(student.id,))
            links.append('<a href="%s">%s</a>' % (change_url, student))
        return format_html("<br>".join(links));
    student_links.short_description = _("Students at this Address")

    def contact_links(self, obj):
        contacts = obj.contact_set.all()
        links = [];
        for contact in contacts:
            change_url = urlresolvers.reverse("admin:people_contact_change", args=(contact.id,))
            links.append('<a href="%s">%s</a>' % (change_url, contact))
        return format_html("<br>".join(links));
    contact_links.short_description = _("Contacts at this Address")



admin.site.register(Address, AddressAdmin)
