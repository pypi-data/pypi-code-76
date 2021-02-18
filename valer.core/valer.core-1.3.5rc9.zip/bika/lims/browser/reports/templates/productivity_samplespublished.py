<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
        i18n:domain="senaite.core"
        tal:define="portal_url nocall:context/portal_url;
        portal portal_url/getPortalObject;">

<head>
    <link rel="stylesheet" type="text/css" media="all" href=""
            tal:attributes="href string:$portal_url/reports.css" />
</head>

<body tal:define="
        report_data view/report_data;
        parameters python:report_data.has_key('parameters') and report_data['parameters'] or [];
        datalines python:report_data.has_key('datalines') and report_data['datalines'] or {};
        footlines python:report_data.has_key('footlines') and report_data['footlines'] or {};">

<!--

Report customization notes
==========================================================================
Available attributes:

   parameters[]

   datalines {
       <analysisrequestid>: {
           AnalysisRequestID,
           DateCreated,
           DateReceived,
           DatePublished,
           ReceptionLag,
           PublicationLag,
           TotalLag,
           SampleID,
           SampleType,
           ClientID,
           BatchID,
           NumAnalyses,
           Creator,
           Remarks,
           VerificationComment
       }
   }

   Where:
   - dict key <analysisrequestid> is the AR ID

   footlines {
       Total: {
           Created,                 - total count of ARs created
           Received,                - total count of ARs received
           Published,               - total count of ARs published
           ReceivedCreatedRatio,    - ratio of AR received amongst created
           ReceivedCreatedRatioPercentage,
           PublishedCreatedRatio,
           PublishedCreatedRatioPercentage
           PublishedReceivedRatio,
           PublishedReceivedRatioPercentage
           AvgReceptionLag,
           AvgPublicationLag,
           AvgTotalLag
           NumAnalyses
       }
   }

-->

<h1 i18n:translate="">Sample Published Report</h1>
<!--            <h3 i18n:translate="">Number of Samples and totals submitted
                                                          between a period of time</h3>
 -->
<!-- Summary -->
<table class="bika-report-parms" summary="Parameters">
    <tr tal:repeat="line parameters">
        <td tal:content="python:line['title']"></td>
        <td tal:content="python:line['value']"></td>
    </tr>
</table>

<!-- Results -->
<table class="bika-report-table" summary="Results">
    <thead>
    <tr>
        <th i18n:translate="">Accession#</th>
        <th i18n:translate="">Date</th>
        <th i18n:translate="">Patient ID#</th>
        <th i18n:translate="">Name</th>
        <th i18n:translate="">Birthdate</th>
        <th i18n:translate="">Doctor</th>
        <th i18n:translate="">Test Result</th>
        <th i18n:translate="">Prev. Acc#</th>
        <th i18n:translate="">Date</th>
        <th i18n:translate="">Prev. Result</th>
    </tr>
    </thead>
    <tbody>
    <metal:block tal:repeat="ar python:datalines.keys()">
        <tr>
            <td tal:content="python:datalines[ar]['AnalysisRequestID']"></td>
            <td tal:content="python:datalines[ar]['DatePublished']"></td>
            <td tal:content="python:datalines[ar]['PatientID']"></td>
            <td tal:content="python:datalines[ar]['PatientName']"></td>
            <td tal:content="python:datalines[ar]['BirthDate']"></td>
            <td tal:content="python:datalines[ar]['Doctor']"></td>
            <td tal:content="python:datalines[ar]['Result']"></td>
            <td tal:content="python:datalines[ar]['PreAnalysisRequestID']"></td>
            <td tal:content="python:datalines[ar]['PreDatePublished']"></td>
            <td tal:content="python:datalines[ar]['PreResult']"></td>
        </tr>
    </metal:block>
    </tbody>
    <tfoot>
    <tr>
        <td colspan="10">&nbsp;</td>
    </tr>
    </tfoot>
</table>
</body>
</html>

