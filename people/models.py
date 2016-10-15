from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

class Contact(models.Model):
    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")

    KIND_CHOICES = (
            ("oth",_("Other")),
            ("fam",_("Family")),
            ("com",_("Company")),
            ("org",_("Organization")),
        )

    name = models.CharField(_("Name"), max_length=200)
    kind = models.CharField(_("Kind"), max_length=3, choices=KIND_CHOICES)

    street = models.CharField(_("Street Address"), max_length=200, blank=True)
    postal_code = models.CharField(_("Postal Code"), max_length=200, blank=True)
    city = models.CharField(_("City"), max_length=200, blank=True)
    country = models.CharField(_("Country"), max_length=200, blank=True)

    def __str__(self):
        return self.name


class Student(models.Model):
    class Meta:
        verbose_name = _("Student")
        verbose_name_plural = _("Students")

    first_name = models.CharField(_("First Name"), max_length=200)
    last_name = models.CharField(_("Last Name"), max_length=200)

    family = models.ForeignKey(Contact, 
                on_delete=models.CASCADE, 
                verbose_name=_("Family"), 
                related_name=_("Students"), 
                limit_choices_to={"kind":"fam"})

    def __str__(self):
        return self.first_name + " " + self.last_name


class PhoneNumber(models.Model):
    class Meta:
        verbose_name = _("Phone Number")
        verbose_name_plural = _("Phone Numbers")

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name=_("Contact"))
    number = models.CharField(_("Phone Number"), max_length=200)
    description = models.CharField(_("Description"), max_length=200, blank=True)

    def __str__(self):
        return self.number


class EMailAddress(models.Model):
    class Meta:
        verbose_name = _("EMail Address")
        verbose_name_plural = _("EMailAddresses")

    contact = models.ForeignKey(Contact, on_delete=models.CASCADE, verbose_name=_("Contact"))
    address = models.CharField(_("Address"), max_length=200)
    description = models.CharField(_("Description"), max_length=200, blank=True)

    def __str__(self):
        return self.number
