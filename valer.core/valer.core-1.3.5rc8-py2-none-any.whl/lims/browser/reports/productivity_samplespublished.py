# -*- coding: utf-8 -*-
#
# This file is part of SENAITE.CORE.
#
# SENAITE.CORE is free software: you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free Software
# Foundation, version 2.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU General Public License for more
# details.
#
# You should have received a copy of the GNU General Public License along with
# this program; if not, write to the Free Software Foundation, Inc., 51
# Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Copyright 2018-2020 by it's authors.
# Some rights reserved, see README and LICENSE.

from bika.lims.workflow import getTransitionDate

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from bika.lims import bikaMessageFactory as _
from bika.lims.browser import BrowserView
from bika.lims.browser.reports.selection_macros import SelectionMacrosView
from plone.app.layout.globals.interfaces import IViewView
from zope.interface import implements
from bika.lims.catalog import CATALOG_ANALYSIS_REQUEST_LISTING
from Products.CMFCore.utils import getToolByName
from bika.lims import logger


class Report(BrowserView):
    implements(IViewView)
    default_template = ViewPageTemplateFile("templates/productivity.pt")
    template = ViewPageTemplateFile("templates/productivity_samplespublished.pt")

    def __init__(self, context, request, report=None):
        super(Report, self).__init__(context, request)
        self.report = report
        self.selection_macros = SelectionMacrosView(self.context, self.request)

    def __call__(self):

        parms = []
        titles = []

        # Apply filters
        self.contentFilter = {'portal_type': 'AnalysisRequest'}
        val = self.selection_macros.parse_daterange(self.request,
                                                    'getDateCreated',
                                                    _('Date Created'))
        if val:
            self.contentFilter["created"] = val['contentFilter'][1]
            parms.append(val['parms'])
            titles.append(val['titles'])

        # Query the catalog and store results in a dictionary
        catalog = getToolByName(self.context, CATALOG_ANALYSIS_REQUEST_LISTING)
        uid_catalog = getToolByName(self.context,'uid_catalog')

        ars = catalog(self.contentFilter)

        logger.info("Catalog Query '{}' returned {} results".format(
            self.contentFilter, len(ars)))

        if not ars:
            message = _("No Samples matched your query")
            self.context.plone_utils.addPortalMessage(message, "error")
            return self.default_template()

        datalines = {}
        footlines = {}
        totalcreatedcount = len(ars)
        totalreceivedcount = 0
        totalpublishedcount = 0
        totalanlcount = 0
        totalreceptionlag = 0
        totalpublicationlag = 0

        for ar in ars:
            brain = ar
            ar = ar.getObject()
            datecreated = ar.created()
            datereceived = ar.getDateReceived()
            datepublished = getTransitionDate(ar, 'publish')
            receptionlag = 0
            publicationlag = 0
            anlcount = len(ar.getAnalyses())

            #patient object
            patient  = uid_catalog(UID=brain.getPatientUID)
            if patient and len(patient) ==1:
                patient = patient[0].getObject()

            #doctor object
            #doctor = uid_catalog(UID=brain.getDoctorTitle)
            #if doctor and le

            #previous test
            old_ar_id = None
            old_ar_date = None
            old_result = None
            ars_old = catalog(getPatientUID=brain.getPatientUID)
            if ars_old and len(ars_old) > 0:
                old = ars_old[0].getObject()
                for an in old.getAnalyses():
                    an = an.getObject()
                    if an.getResult():
                        old_result = an.getFormattedResult()

            #getting test result
            for an in  ar.getAnalyses():
                analysis = an.getObject()
                result = analysis.getFormattedResult()

            dataline = {
                "AnalysisRequestID": ar.getId(),
                "DatePublished": self.ulocalized_time(datepublished),
                "PatientID": patient.getClientPatientID(),
                "PatientName": patient.getFullname(),
                "BirthDate": patient.getBirthDate(),
                "Doctor": brain.getDoctorTitle,
                "Result": result,
                "PreAnalysisRequestID": old_ar_id,
                "PreDatePublished": old_ar_date,
                "PreResult": old_result,
            }

            datalines[ar.getId()] = dataline


        footlines['Total'] = ''

        self.report_data = {'parameters': parms,
                            'datalines': datalines,
                            'footlines': footlines}

        if self.request.get('output_format', '') == 'CSV':
            import csv
            import StringIO
            import datetime

            fieldnames = [
                "AnalysisRequestID",
                "DatePublished",
                "PatientID",
                "PatientName",
                "BirthDate",
                "Doctor",
                "Result",
                "PreAnalysisRequestID",
                "PreDatePublished",
                "PreResult",
            ]
            output = StringIO.StringIO()
            dw = csv.DictWriter(output, extrasaction='ignore',
                                fieldnames=fieldnames)
            dw.writerow(dict((fn, fn) for fn in fieldnames))
            for ar_id, row in datalines.items():
                dw.writerow({
                    "AnalysisRequestID": row["AnalysisRequestID"],
                    "DatePublished": row["DatePublished"],
                    "PatientID": row["PatientID"],
                    "PatientName": row["PatientName"],
                    "BirthDate": row["BirthDate"],
                    "Doctor": row["Doctor"],
                    "Result": row["Result"],
                    "PreAnalysisRequestID": row["PreAnalysisRequestID"],
                    "PreDatePublished": row["PreDatePublished"],
                    "PreResult": row["PreResult"],
                })
            report_data = output.getvalue()
            output.close()
            date = datetime.datetime.now().strftime("%Y%m%d%H%M")
            setheader = self.request.RESPONSE.setHeader
            setheader('Content-Type', 'text/csv')
            setheader("Content-Disposition",
                      "attachment;filename=\"samples_published_%s.csv\"" % date)
            self.request.RESPONSE.write(report_data)
        else:
            return {'report_title': _('Data entry day book'),
                    'report_data': self.template()}

