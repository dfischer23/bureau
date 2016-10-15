from django.contrib import admin
from django.core import urlresolvers
from django.utils.html import format_html
from django.http import HttpResponse
from django.utils.translation import ugettext as _

from .models import *


class StudentAdmin(admin.ModelAdmin):
    model = Student
    list_display = ("get_full_name", "get_family")
    search_fields = ["first_name", "last_name"]

    def get_full_name(self, obj):
        return obj.first_name + " " + obj.last_name;
    get_full_name.short_description = _("Name")

    def get_family(self, obj):
        return obj.family.name;
    get_family.short_description = _("Familie")

admin.site.register(Student, StudentAdmin)


class StudentInline(admin.TabularInline):
    extra = 0
    model = Student

class PhoneNumberInline(admin.TabularInline):
    extra = 0
    model = PhoneNumber

class EMailAddressInline(admin.TabularInline):
    extra = 0
    model = EMailAddress



def export_csv(modeladmin, request, queryset):
    import csv
    from django.utils.encoding import smart_str
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=test.csv'
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))
    writer.writerow([
        smart_str(_("ID")),
        smart_str(_("Name")),
        smart_str(_("Phone Numbers")),
    ])
    for obj in queryset:
        writer.writerow([
            smart_str(obj.pk),
            smart_str(obj.name),
            smart_str(obj.phonenumber_set.all())
        ])
    return response
export_csv.short_description = _("Export CSV")


class ContactAdmin(admin.ModelAdmin):
    model = Contact
    inlines = [
        StudentInline,
        PhoneNumberInline,
        EMailAddressInline
    ]
    actions = [export_csv]
    list_display = ("name","kind","city","country")
    search_fields = ["name"]
    list_filter = ("kind",)

admin.site.register(Contact, ContactAdmin)


#class FamilyAdmin(admin.ModelAdmin):
#    model = Family
#    inlines = [
#        PersonInline,
#        PhoneNumberInline
#    ]

#    readonly_fields = ("family_members",)
#    fields = ("name","family_members")

#    def family_members(self, obj):
#        members = Person.objects.filter(family=obj)
#        if members.count()==0:
#            return '(none)'
#        output = ", ".join([str(member) for member in members])
#        return output
#
#        member_links = []
#        for member in members:
#            change_url = urlresolvers.reverse("admin:people_person_change", args=(member.id,))
#            member_links.append('<a href="%s">%s</a>' % (change_url, member.first_name))
#        return format_html(", ".join(member_links))
#    family_members.allow_tags = True
#    family_members.verbose_name = _("Family Members")

#admin.site.register(Family, FamilyAdmin)
