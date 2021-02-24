#  Copyright (C) 2020 <Florian Alu - Prolibre - https://prolibre.com
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.
#
#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.

from django.core.management.base import BaseCommand



# from config.wsgi import logger


class Command(BaseCommand):
	help = "Command for set agegroup auto"

	# def add_arguments(self, parser):
	#     parser.add_argument('sample', nargs='+')
	def handle(self, *args, **options):

from nobinobi_child.models import Contact
for ct in Contact.objects.all():
	p = str(ct.phone)
	mp = str(ct.mobile_phone)
	pp = str(ct.professional_phone)
	if p:
		if "." in p:
			p = p.replace(".", "")
		if "/" in p:
			p = p.replace("/", "")
		if " " in p:
			p = p.replace(" ", "")
		ct.phone = p
	if mp:
		if "." in mp:
			mp = mp.replace(".", "")
		if "/" in mp:
			mp = mp.replace("/", "")
		if " " in mp:
			mp = mp.replace(" ", "")
		ct.mobile_phone = mp
	if pp:
		if "." in pp:
			pp = pp.replace(".", "")
		if "/" in pp:
			pp = pp.replace("/", "")
		if " " in pp:
			pp = pp.replace(" ", "")
		ct.professional_phone = pp
	ct.save()






for ct in Contact.objects.all():
	p = str(ct.phone)
	mp = str(ct.mobile_phone)
	pp = str(ct.professional_phone)
	if p:
		if p.startswith("022"):
			p = p.replace("022", "+4122")
		if p.startswith("076"):
			p = p.replace("076", "+4176")
		if p.startswith("078"):
			p = p.replace("078", "+4178")
		if p.startswith("079"):
			p = p.replace("079", "+4179")
		ct.phone = p
	if mp:
		if mp.startswith("022"):
			mp = mp.replace("022", "+4122")
		if mp.startswith("076"):
			mp = mp.replace("076", "+4176")
		if mp.startswith("078"):
			mp = mp.replace("078", "+4178")
		if mp.startswith("079"):
			mp = mp.replace("079", "+4179")
		ct.mobile_phone = mp
	if pp:
		if pp.startswith("022"):
			pp = pp.replace("022", "+4122")
		if pp.startswith("076"):
			pp = pp.replace("076", "+4176")
		if pp.startswith("078"):
			pp = pp.replace("078", "+4178")
		if pp.startswith("079"):
			pp = pp.replace("079", "+4179")
		ct.professional_phone = pp
	ct.save()




for ct in Contact.objects.all():
	p = str(ct.phone)
	mp = str(ct.mobile_phone)
	pp = str(ct.professional_phone)
	if mp:
		if mp == "-" or mp == "None":
			mp = None
		ct.mobile_phone = mp
	if pp:
		if pp == "-" or pp == "None":
			pp = None
		ct.professional_phone = pp
	ct.save()


