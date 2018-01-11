from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from .models import Student, Contact
from django.shortcuts import render

import csv
from django.http import HttpResponse

from io import BytesIO
from xlsxwriter.workbook import Workbook

@login_required
def index(request):
    return render(request, 'students.html', 
        {'students': Student.objects.all() })

@login_required
def list_excel(request):
	output = BytesIO()
	book = Workbook(output)
	sheet = book.add_worksheet("Adressliste")

	format_normal = book.add_format({"font_size": 8, "bold": False, "num_format": "dd.mm.yyyy"})
	format_normal_gray = book.add_format({"font_size": 8, "bold": False, "num_format": "dd.mm.yyyy", "bg_color":"#CCCCCC"})
	format_bold = book.add_format({"font_size": 8, "bold": True, "num_format": "dd.mm.yyyy"})
	format_bold_gray = book.add_format({"font_size": 8, "bold": True, "num_format": "dd.mm.yyyy", "bg_color":"#CCCCCC"})

	printed = []
	row = 1
	gray = False

	sheet.set_column(0,1,15)
	sheet.set_column(2,1,7)
	sheet.set_column(3,10,15)

	for student in Student.objects.all().filter(status="active"):

		if not student.id in printed:
			gray = not gray

			# get this student's guardians
			guardians = student.guardians.all()

			# actually print the first guardians's students
			for child in guardians[0].students.all().filter(status="active"):
				sheet.write(row, 0, child.name)
				sheet.write(row, 1, child.first_name)
				sheet.write_datetime(row, 2, child.dob)
				sheet.set_row(row, 10, format_bold_gray if gray else format_bold)
				printed.append(child.id)
				row += 1


			# print all guardians
			for guardian in guardians:
				sheet.write(row, 0, guardian.name)
				sheet.write(row, 1, guardian.first_name)
				sheet.write(row, 2, "")
				sheet.write(row, 3, guardian.address.street)
				sheet.write(row, 4, guardian.address.postal_code+" "+guardian.address.city)
				sheet.write(row, 5, guardian.phone_number)
				sheet.write(row, 6, guardian.cellphone_number)
				sheet.write(row, 7, guardian.email_address)
				sheet.set_row(row, 10, format_normal_gray if gray else format_normal)
				row += 1

	row += 1
	for person in Contact.objects.all().filter(is_teammember=True):
				sheet.write(row, 0, person.name)
				sheet.write(row, 1, person.first_name)
				sheet.write(row, 2, "")
				sheet.write(row, 3, person.address.street)
				sheet.write(row, 4, person.address.postal_code+" "+person.address.city)
				sheet.write(row, 5, person.phone_number)
				sheet.write(row, 6, person.cellphone_number)
				sheet.write(row, 7, person.team_email_address)
				sheet.set_row(row, 10, format_normal)
				row += 1


	book.close()

	output.seek(0)
	response = HttpResponse(output.read(), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
	response['Content-Disposition'] = "attachment; filename=adressliste.xlsx"

	return response

# for testing only
@login_required
def list_csv(request):
		response = HttpResponse(content_type="text/csv")
		response["Content-Disposition"] = "attachment;filename=list.csv"

		writer = csv.writer(response)
		writer.writerow(["Name", "Vorname", "Geburtsdatum", "Strasse", "Ort", "Telefon", "Handy", "E-Mail"])

		printed = []

		for student in Student.objects.all():

			if not student.id in printed:
				# get this student's guardians
				guardians = student.guardians.all()

				# actually print the first guardians's students
				for child in guardians[0].students.all():
					writer.writerow([child.name, child.first_name, child.dob.strftime("%d.%m.%Y")])
					printed.append(child.id)


				# print all guardians
				for guardian in guardians:
					writer.writerow([guardian.name, guardian.first_name, "",
						guardian.address.street, guardian.address.postal_code+" "+guardian.address.city,
						guardian.phone_number, guardian.cellphone_number, guardian.email_address
						])


		return response;

#@login_required
def students_csv(request, status="active"):
		response = HttpResponse(content_type="text/csv")
		response["Content-Disposition"] = "attachment;filename=list.csv"

		writer = csv.writer(response)

		writer.writerow(["SchülerInnen mit Status '"+status+"'", "Stand:", "---"]);
		writer.writerow(["Name", "Vorname", "Geburtsdatum", "Strasse", "Ort", "Erziehungsberechtigte"])

		for student in Student.objects.all().filter(status=status):
			guardian_names = [];
			first_guardian_name = ""
			for guardian in student.guardians.all():
				if first_guardian_name == guardian.name:
					guardian_names.append(guardian.first_name);
				else:
					first_guardian_name = guardian.name;
					guardian_names.append(guardian.first_name + " " + guardian.name);

			guardian_names.reverse()

			writer.writerow([student.name, student.first_name, student.dob.strftime("%d.%m.%Y"), 
				student.address.street, student.address.postal_code+" "+student.address.city,
				" und ".join(guardian_names)])

		return response;
