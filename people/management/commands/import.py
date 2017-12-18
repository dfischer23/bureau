from django.core.management.base import BaseCommand, CommandError
from people.models import Student, Contact, Address

import csv
import re
from datetime import datetime

# Eingangsnummer,Schulvertrag Nummer,Datenschutzerklärung,Infektionsschutzgesetz,Platzhalter Elterngespräch,Anmerkung,
# Name Schüler,Vorname/n,Geburtsdatum,Alter Einschulung,Warteliste,Klassenstufe 13/14,Klassenstufe 16/17,
# Geburtsort,Geschlecht,Staatsangehörigkeit,Konfession,Zusatz,Straße,Stadt,Frei 1,
# Name Erziehungsberechtigter A,Vorname A,Zusatz A,Straße A,Stadt A,Telefon A,Mobil A,E-Mail A,Frei 2,
# Name Erziehungsberechtigter B,Vorname B,Zusatz B,Straße B,Stadt B,Telefon B,Mobil B,E-Mail B,Frei 3,
# Anschrift 1,Zusatz Brief,Anschrift 2,Anschrift 3,Anrede,,


class Command(BaseCommand):
	help = 'Import data from CSV'

	def add_arguments(self, parser):
		parser.add_argument("filename")

	def handle(self, *args, **options):
		filename = options["filename"]

		with open(filename, "r") as file:
			reader = csv.DictReader(file, delimiter=",", quotechar="\"")
			for row in reader:

				entry_nr = int(row["Eingangsnummer"])
				student, created = Student.objects.get_or_create(entry_nr=entry_nr);

				contract_nr = row["Schulvertrag Nummer"];
				student.contract_nr = int(contract_nr) if contract_nr else None

				if row["Geschlecht"] == "m": student.gender = "m";
				if row["Geschlecht"] == "w": student.gender = "f";
				student.denomination = row["Konfession"]
				student.citizenship = row["Staatsangehörigkeit"]

				student.status = "active";

				student.level_ref = 2016;
				student.level_ofs = int(row["Klassenstufe 16/17"]);
				student.first_enrollment = 2017 - int(row["Klassenstufe 16/17"]);

				student.privacy_policy_agreement = (row["Datenschutzerklärung"] != "")
				student.vaccination_policy_agreement = (row["Infektionsschutzgesetz"] != "");

				# student.is_sibling TODO

				student.first_name = row["Vorname/n"]
				student.name = row["Name Schüler"]
				student.short_name = student.first_name.split()[0]+" "+student.name[0];
				student.dob = datetime.strptime(row["Geburtsdatum"], "%m/%d/%y")
				student.pob = row["Geburtsort"];

				student.address = self.add_address(row["Straße"], row["Stadt"])

				self.add_guardian(student, row["Name Erziehungsberechtigter A"], row["Vorname A"], row["Straße A"], row["Stadt A"], row["Telefon A"], row["Mobil A"], row["E-Mail A"]);
				self.add_guardian(student, row["Name Erziehungsberechtigter B"], row["Vorname B"], row["Straße B"], row["Stadt B"], row["Telefon B"], row["Mobil B"], row["E-Mail B"]);

				student.save();

				# todo: check unprocessed fields for entries

	def add_guardian(self, student, name, first_name, street, city, phone, mobile, email):
		if name:
#			self.stdout.write("Add guardian %s %s for %s" % (first_name, name, student.first_name));

			addr = self.add_address(street, city)

			contact, created = Contact.objects.get_or_create(
				name=name, first_name=first_name, kind="prs", 
				address=addr)

			phone = self.normalize_phone(phone);
			mobile = self.normalize_phone(mobile);

			if not created:
				if contact.phone_number != phone:
					self.stdout.write(self.style.WARNING("Contact '%s' exists, but with different Phone Number: %s / %s; overwriting!" % (contact, contact.phone_number, phone)))
				if contact.cellphone_number != mobile:
					self.stdout.write(self.style.WARNING("Contact '%s' exists, but with different Mobile Phone Number: %s / %s; overwriting!" % (contact, contact.cellphone_number, mobile)))

			contact.phone_number = phone;
			contact.cellphone_number = mobile;
			contact.email_address = email;

			contact.save();

			student.guardians.add(contact);

	def normalize_phone(self, number):
		return number.replace("–","-").replace(" ","").replace("o.", " oder ");

	def add_address(self, str, code_and_city):
		street = str.replace("tr.", "traße");

		m = re.match("(\d+)\ (.+)", code_and_city)
		code = m.group(1)
		city = m.group(2)

		address, created = Address.objects.get_or_create(street=street, postal_code=code, city=city, country="Germany");

		address.save();
		return address;


#    street = models.CharField(_("Street Address"), max_length=200, blank=True)
#    postal_code = models.CharField(_("Postal Code"), max_length=200, blank=True)
#    city = models.CharField(_("City"), max_length=200, blank=True)

#    alternative = models.CharField(_("Alternative"), max_length=1000, blank=True)

#    country = models.CharField(_("Country"), max_length=200, blank=True)



