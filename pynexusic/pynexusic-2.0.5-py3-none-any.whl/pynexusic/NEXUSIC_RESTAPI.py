import requests
import base64
import datetime
import traceback
import json

SCRIPT_VERSION = '2.0.5'

############################# NEXUS REST API V2 Functions ############################
class NEXUSIC_REST():
    """
    NEXUS IC REST API class allows the user to communicate with Wood NEXUS IC REST API using python.

    Version: 2.0.5

    Prerequisites:
    -------------
        - Python > 3.6
        - NEXUS IC V6.6
        - IC-Web V6.6

    NEXUS IC Documentation:
    ----------------------
        The NEXUS IC REST API documentation can be found in the below link:
        https://docs.nexusic.com/6.6/ic-web.rest.v2.html

        A specific NEXUS IC version can be specified in the above link by changing **6.6** to the desired NEXUS IC version*
    """

    _error_msgs = ['An existing connection was forcibly closed by the remote host',
                   'Remote end closed connection without response']

    def __init__(self, icweb_uri, authentication_type='APIKEY',
                 username=None, password=None, api_key=None,
                 max_attempts=1, timeout=None, verbose=False, verify=True):
        """
            The constructor for NEXUSIC_REST class.

            Parameters:
            ----------
                icweb_uri (string): IC-Web URL.
                authentication_type (string - optional): This can be either APIKEY or BASIC (default value APIKEY).
                username (string - optional): Default value None.
                password (string - optional): Default value None.
                api_key (string - optional): Default value None.
                max_attempts (int - optional): Maximum number of attempts if disconnected (default value 1).
                timeout (int - optional): Timeout threshold in seconds (default value None).
                verbose (bool - optional): Print internal messages if True (default value False).
                verify (bool - optional): By pass SSL verification if True (default value False).

            Returns:
            -------
                None
            """

        self.icweb_uri = icweb_uri
        self.authentication_type = authentication_type

        self.api_key = api_key
        self.username = username
        self.password = password

        self.max_attempts = max_attempts
        self.timeout = timeout   # TODO: To be added to the REST calls
        self.verbose = verbose
        self.verify = verify

        assert authentication_type in ['APIKEY', 'BASIC'], 'Incorrect authentication type'

        if authentication_type == 'APIKEY':
            if self.api_key != None:
                self.key_64 = self.generate_base64(api_key)
            else:
                raise Exception('API Key is not valid, please provide a valid API Key')
        elif authentication_type == 'BASIC':
            if self.username != None or self.password != None:
                self.key_64 = self.generate_base64(self.username + ':' + self.password)
            else:
                raise Exception('Username and/or password are not valid, please provide a valid username/password')
        else:
            raise Exception('Authentication type was not specified')

        self.hash = self.generate_hash()

        # Get current NEXUS version
        version, version_status_code = self.getVersion()
        self.version = version['version'].split('.')
        self.schema = version['schema'].split('.')

    ######################################################################################
    def generate_base64(self, value):
        return str(base64.b64encode(bytes(value, 'utf-8')), "utf-8")

    ######################################################################################
    def generate_hash(self, verbose=False):
        result, result_code = self.authenticate(verbose=verbose)

        if result_code == 200:
            return result.get('hash')
        else:
            errorMsg = traceback.format_exc()
            raise Exception(result + '\n' + errorMsg)

    ######################################################################################
    def validate_and_return_response(self, response, message, raw=False):
        if response.status_code == 200:
            if raw:
                return response.raw, response.status_code
            else:
                return response.json(), response.status_code
        else:
            return str(message) + str(response.status_code) + ': ' + str(response.text), \
                   response.status_code

    ######################################################################################
    def authenticate(self, verbose=False):
        if self.verbose or verbose:
            print('Authenticating with NEXUS IC...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/security/login'
        res = requests.get(uri, headers={'Authorization': self.authentication_type + ' ' + self.key_64},
                           verify=self.verify)

        return self.validate_and_return_response(res, 'Authentication error ')

    ######################################################################################
    def getVersion(self, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting NEXUS IC version...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/version' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get version error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getVersion(current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getTable(self, tableName, xFilter=None, pageSize=None, current_attempt=1,
                 verbose=False):
        if self.verbose or verbose:
            print('Getting ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        if pageSize == None:
            uri = baseURI + '/bo/' + tableName + '/' + '?hash=' + self.hash
        else:
            uri = baseURI + '/bo/' + tableName + '/' + '?pageSize=' + str(pageSize) + '&hash=' + self.hash

        try:
            if xFilter != None:
                res = requests.get(uri, headers={'X-NEXUS-Filter': xFilter}, verify=self.verify)
            else:
                res = requests.get(uri, verify=self.verify)

            result, result_code = self.validate_and_return_response(res, 'Get ' + tableName + ' table error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getTable(tableName, xFilter=xFilter, pageSize=pageSize,
                                        current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def deleteRecord(self, tableName, keyValue, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Deleting from ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableName + '/' + str(keyValue) + '/' + '?hash=' + self.hash

        try:
            res = requests.delete(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Delete ' + tableName + ' table error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.deleteRecord(tableName, keyValue, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getMultimedia(self, rd_id, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Getting multimedia: ' + str(rd_id) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        xFilter = str(rd_id) + '/File_Data'
        uri = baseURI + '/bo/' + 'Repository_Data' + '/' + xFilter + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, stream=True, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get multimeida error ', raw=True)
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getMultimedia(rd_id, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    # V6.6 only
    def getDashboard(self, dashboard_Name, current_attempt=1, verbose=False):
        # Check if minor version is 6
        if not(int(self.version[1]) >= 6):
            return 'This function is not supported in the current NEXUS IC version', 404

        if self.verbose or verbose:
            print('Generating NEXUS IC dashboard...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + dashboard_Name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/dashboard/' + str(rt_id) + '/' + '?hash=' + self.hash

        try:
            res = requests.get(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Get ' + dashboard_Name + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.getDashboard(dashboard_Name, current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def generateReport(self, report_name, recipient, format='XLSX', current_attempt=1,
                       verbose=False):
        if self.verbose or verbose:
            print('Generating NEXUS IC report...')

        # Get RT_ID
        xFilter = '{"where": [{"field": "Name", "value": "' + report_name + '"}]}'
        report_json, report_status = self.getTable('Report_Template', xFilter=xFilter)

        if report_status == 404:
            return str(report_status) + ': ' + str(report_json), report_status
        else:
            rt_id = report_json['rows'][0]['RT_ID']

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        # Generate report
        uri = baseURI + '/web/generateReport'
        uri += '?key=' + str(rt_id) + '&format=' + format + '&recipient=' + recipient + '&hash=' + self.hash

        try:
            res = requests.post(uri, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Generate ' + report_name + ' report error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.generateReport(report_name, recipient, format=format,
                                              current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execFunction(self, functionName, parameters=None, current_attempt=1,
                     verbose=False):
        if self.verbose or verbose:
            print('Executing ' + str(functionName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/function/' + functionName
        uri += '/' + '?hash=' + self.hash

        try:
            res = requests.post(uri, json=parameters, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Execute function ' + functionName + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.execFunction(functionName, parameters=parameters,
                                            current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def execUpdate(self, tableName, tableID, body, current_attempt=1, verbose=False):
        if self.verbose or verbose:
            print('Updating ' + str(tableName) + '...')

        # Adding /data/icweb.dll part to the baseURI
        baseURI = self.icweb_uri + '/data/icweb.dll'

        uri = baseURI + '/bo/' + tableName + '/' + tableID
        uri += '?hash=' + self.hash

        try:
            res = requests.post(uri, json=body, verify=self.verify)
            result, result_code = self.validate_and_return_response(res, 'Updating ' + tableName + ' error ')
            return result, result_code
        except Exception as e:
            for error_msg in NEXUSIC_REST._error_msgs:
                if error_msg in str(e):
                    current_attempt += 1
                    if (current_attempt <= self.max_attempts) and not (self.key_64 == None):
                        self.hash = self.generate_hash()
                        return self.execUpdate(tableName, tableID, body,
                                          current_attempt=current_attempt)

            errorMsg = traceback.format_exc()
            raise Exception('Number of attempts: ' + str(current_attempt) + '\n' + errorMsg)

    ######################################################################################
    def getAssetLocationByName(self, assetName, assetView,
                         pageSize=None, current_attempt=1, verbose=False):
        x_filter = {"operator": "and",
                    "where": [{"field": "Comp_View.Name", "value": assetView},
                              {"field": "Component.Name", "value": assetName}]
                    }

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize,
                                               current_attempt=current_attempt, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetLocationByID(self, assetID, assetView,
                         pageSize=None, current_attempt=1, verbose=False):
        x_filter = {"operator": "and",
                    "where": [{"field": "Comp_View.Name", "value": assetView},
                              {"field": "Component.Component_ID", "value": assetID}]
                    }

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize,
                                               current_attempt=current_attempt, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetChildren(self, assetLocation, assetView=None, searchType='MAX LEVEL', assetTypes=None,
                         maxLevel=-1, atLevel=-1, pageSize=None, current_attempt=1, verbose=False):
        assert searchType in ['MAX LEVEL', 'AT LEVEL'], 'Incorrect search type'

        x_filter = {"operator": "and",
                    "where": [{"field": "View_Node.VN_ID", "method": "ch", "value": assetLocation}]
                    }

        # Apply asset view filter
        if assetView != None:
            x_filter['where'].append({"field": "Comp_View.Name", "value": assetView})

        # Apply asset type filters
        if assetTypes != None:
            # Get asset type IDs
            assetTypeIDs = self.getAssetTypesID(assetTypes, current_attempt=current_attempt,
                                                pageSize=pageSize, verbose=verbose)

            # Asset children filter
            x_filter['where'].append({"field": "CT_ID", "method": "in", "items": assetTypeIDs})

        # Apply level filter
        if searchType == 'MAX LEVEL' and maxLevel != -1:
            x_filter['where'].append({"field": "Level", "method": "le", "value": maxLevel})
        elif searchType == 'AT LEVEL' and atLevel != -1:
            x_filter['where'].append({"field": "Level", "value": atLevel})

        x_filter = json.dumps(x_filter)

        result, result_code = self.getTable('View_Node', xFilter=x_filter, pageSize=pageSize,
                                               current_attempt=current_attempt, verbose=verbose)

        return result, result_code

    ######################################################################################
    def getAssetTypesID(self, assetTypes, current_attempt=1, pageSize=None, verbose=False):
        assetTypeIDs = []
        for assetType in assetTypes:
            at_x_filter = {"where": [{"field": "Name", "value": assetType}]}
            at_x_filter = json.dumps(at_x_filter)
            result, result_code = self.getTable('Comp_Type', xFilter=at_x_filter, pageSize=pageSize,
                                                   current_attempt=current_attempt, verbose=verbose)

            if len(result['rows']) != 0:
                assetTypeIDs.append(result['rows'][0]['CT_ID'])
            else:
                assetTypeIDs.append('Asset type does not exist in the database')

        return assetTypeIDs

    ######################################################################################
    def getTableDBNames(self, tableNames, tableType, current_attempt=1,
                        pageSize=None, verbose=False):
        tableDBNames = []

        for tableIndex, tableName in enumerate(tableNames):
            x_filter = {"operator": "and",
                        "where": [{"field": "Name", "value": tableName},
                                  {"field": "Def_Type.Name", "value": tableType}]
                        }
            x_filter = json.dumps(x_filter)

            result, result_code = self.getTable('Table_Def', xFilter=x_filter,pageSize=pageSize,
                                                current_attempt=current_attempt, verbose=verbose)

            for row in result['rows']:
                tableDBNames.append(row['Table_Name'])

        return tableDBNames

######################################################################################
################################### Start Script #####################################
if __name__ == '__main__':
    baseURI = ''
    apiKey = ''

    startTime = datetime.datetime.now()

    ## Program start here
    print(NEXUSIC_REST.__doc__)
    ## End of program

    endTime = datetime.datetime.now()
    elapsedTime = endTime - startTime

    print('NEXUS IC REST API actions completed.....runtime: %s' % (str(elapsedTime)))


