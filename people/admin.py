from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from .models import *
from django import forms

from datetime import date

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
    list_display = ("short_name", "name", "first_name", "calc_level", "status")
    search_fields = ["first_name", "name"]
    list_filter = ("status",)
    filter_horizontal = ("guardians",)
    readonly_fields = ("guardians_links","calc_level")
    inlines = [
       NoteInline,
    ]

    fieldsets = (
    	(None, {
    		"fields": ("short_name", "name", "first_name", "status", "dob", "pob", "address", "guardians_links")
    		}),
    	(_("Class Level"), {
    		"fields":(
    			"first_enrollment",
    			"calc_level",
    			"level_ofs", "level_ref"
    		)}),
    	(_("Formalities"), {
    		"classes":("collapse",),
    		"fields":(
    			"gender",
    			"entry_nr", "contract_nr", 
    			"citizenship", "denomination",
    			"privacy_policy_agreement", "vaccination_policy_agreement", "is_sibling"
    		)}),
    	(_("Edit Guardians"), {
    		"classes":("collapse",),
    		"fields": (
    			"guardians",
    		)})
    	)

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

admin.site.register(Student, StudentAdmin)



#class ContactInline(admin.TabularInline):
#    extra = 0
#    model = Contact
#    classes = ["collapse"]

#class StudentAddressInline(admin.TabularInline):
#    extra = 0
#    model = Student
#    fields = ("name", "first_name")


# def export_csv(modeladmin, request, queryset):
#     import csv
#     from django.utils.encoding import smart_str
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename=test.csv'
#     writer = csv.writer(response, csv.excel)
#     response.write(u'\ufeff'.encode('utf8'))
#     writer.writerow([
#         smart_str(_("ID")),
#         smart_str(_("Name")),
#         smart_str(_("Phone Numbers")),
#     ])
#     for obj in queryset:
#         writer.writerow([
#             smart_str(obj.pk),
#             smart_str(obj.name),
#             smart_str(obj.phonenumber_set.all())
#         ])
#     return response
# export_csv.short_description = _("Export CSV")


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    list_display = ("name","first_name","kind","phone_number","cellphone_number","email_address")
    search_fields = ["name"]
    list_filter = ("kind",)
    readonly_fields = ("student_links",)

    fieldsets = (
        (None, {
            "fields": ("name", "first_name", "kind", "address", "phone_number", "cellphone_number", "email_address", "is_teammember", "team_email_address", "student_links")
            }),
        );

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
