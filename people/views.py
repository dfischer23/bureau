from django.utils.translation import ugettext as _
from django.contrib.auth.decorators import login_required

from .models import Student, Contact
from django.shortcuts import render, get_object_or_404

import csv
from django.http import HttpResponse

from io import BytesIO
from xlsxwriter.workbook import Workbook

@login_required
def index(request):
    return render(request, 'students.html', 
        {'students': Student.objects.all() })

@login_required
def studentcoversheet(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    return render(request, 'studentcoversheet.html', 
        {'student': student })

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
				sheet.write(row, 1, child.short_name if child.short_name else child.first_name )
				sheet.write_datetime(row, 2, child.dob)
				sheet.set_row(row, 10, format_bold_gray if gray else format_bold)
				printed.append(child.id)
				row += 1


			# print all guardians
			for guardian in guardians.filter(on_address_list=True):
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

@login_required
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



from datetime import date, datetime
import math
from django.db.models import Q

def calc_level(student, cutoff_date):
	if not student.level_ref or not student.level_ofs:
		return "N/A"
	current_year = cutoff_date.year-1 if cutoff_date.month < 8 else cutoff_date.year
	level =  current_year - (int(student.level_ref) - int(student.level_ofs))
	return(level)


@login_required
def level_report(request):
		response = HttpResponse(content_type="text/plain; charset=utf-8")
#		response["Content-Disposition"] = "attachment;filename=list.csv"


		# we want to group into two levels (primary 1-4/secondary 5-9)
		groups = [ range(1,5), range(5,10) ]

		# iterate a school year, produce a list of dates, one for each month
		year = 2010
		report_duration = 9
		first_month_of_schoolyear = 6
		dates = list(map(
					lambda month: date(year + math.floor(month/12), (month%12)+1, 1), 
					range(first_month_of_schoolyear-1, first_month_of_schoolyear+(12*report_duration))))

		response.write("Bericht Klassenstufen (%r - %r)\n\n" % (year, year+report_duration));

		enrollment_at_date = ()

		last_students = []

		# now for each of those dates
		for cutoff_date in dates:
			enrolled_at_level = {}
			response.write("%s:\n" % cutoff_date.strftime("%m/%Y"))

			came = []
			left = []

			# and each active student
			for student in Student.objects.all().filter(Q(status="active") | Q(status="alumnus")):
				# if the student doesnt have a first_day, construct it from first_enrollment
				if not student.first_day:
					student.first_day = date(student.first_enrollment, 8, 1)
					#maybe: student.save();

				# see if the student was enrolled
				enrolled_before = not student.first_day or student.first_day <= cutoff_date
				enrolled_after = not student.last_day or student.last_day >= cutoff_date
				enrolled = enrolled_before and enrolled_after

				if enrolled:
					# calculate the students class level at that date
					level = calc_level(student, cutoff_date)

					# create a list at that level if it doesnt exist
					if not level in enrolled_at_level: enrolled_at_level[level] = []

					# add the student to its level
					enrolled_at_level[level].append(student)

					# if she's not in last_students, she "came"
					if not student in last_students:
						came.append(student)
						last_students.append(student)

				else:
					# if she's in last_students, she "left"
					if student in last_students:
						left.append(student)
						last_students.remove(student)

				# just print that info
#				response.write("\t%s %r %r\n" % ("✓" if enrolled else "✗", level, student) );

			# print those that came or left
			if came:
				response.write("\tZugegangen:\n")
				for student in came:
					response.write("\t\t%s, %s (%s)\n" % (student.name, student.first_name, student.first_day.strftime("%d.%m.%Y")))
					
			if left:
				response.write("\tAbgegangen:\n")
				for student in left:
					response.write("\t\t%s, %s (%s)\n" % (student.name, student.first_name, student.last_day.strftime("%d.%m.%Y")))

			# now, for this date, we group
			for group in groups:
				count = 0
				for level in group:
					if level in enrolled_at_level:
						count += len(enrolled_at_level[level])

				response.write("  %i-%i : %r\n" % (group.start, group.stop-1, count))
					

#			response.write("%r\n" % enrolled_at_level)
			response.write("\n")

			# no


		# iterate students
#		for student in Student.objects.all().filter(status="active"):
#			response.write( student.name+", "+student.first_name+" "+calc_level(student)+"\n");


		return response;

