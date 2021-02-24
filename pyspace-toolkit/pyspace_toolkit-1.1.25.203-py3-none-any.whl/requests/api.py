import requests
import json


######################################
# DoccanoClient
import copy
import os
import datetime
from urllib.parse import urljoin
######################################

class MaxiGatewayAPI:
    def __init__(self, url='http://127.0.0.1:5005/model/parse'):
        self.url = url
        self.sender_count = 0

    def query(self, text, sender='api_default'):
        if text == '':
            return {'intent':{'name':'EMPTY TEXT','confidence':0.0}}
        if not isinstance(text, str):
            return {'intent':{'name':'NOT TEXT','confidence':0.0}}

        data = {"text": text, "lang": "tr", "sender_id":sender}
        resp = requests.post(self.url, json = data, verify=False )
        # data = json.dumps(data)
        # resp = requests.post(self.url, data = data, verify=False )
        return resp.json()
    
    def query_with_unique_sender(self, text):
        unique_sender = str(self.sender_count)
        self.sender_count += 1

        return self.query(text, unique_sender)

class RasaAPI:
    # url = 'https://rasa-hascore-service.apps.generic.kube.uatisbank/model/parse'
    # url = 'http://127.0.0.1:5005/model/parse'
    # url = 'https://bilmis-bot-rasacore-service.apps.generic.kube.isbank/model/parse'
    # url = 'http://oguzhankarahan-c54dacea.localhost.run/model/parse'
    # url = 'http://104.40.139.168:5005/model/parse'

    def __init__(self, url='http://127.0.0.1:5005/model/parse', nlg_url='http://127.0.0.1:5005/webhooks/rest/webhook'):
        self.url = url
        self.nlg_url = nlg_url

    def query(self, text):
        if text == '':
            return {'intent':{'name':'EMPTY TEXT','confidence':0.0}}
        if not isinstance(text, str):
            return {'intent':{'name':'NOT TEXT','confidence':0.0}}

        data = {"text": text, "lang": "tr"}
        data = json.dumps(data)
        resp = requests.post(self.url, data = data, verify=False )
        return resp.json()
    
    
    def minified_query(self, text, entity_filters=None):
        resp = self.query(text)

        if entity_filters and isinstance(entity_filters,list):            
            resp['entities'] = [e for e in resp['entities'] if e['entity'] in entity_filters]

        resp['entities'] = [{'entity':e['entity'], 'value':e['value']} for e in resp['entities']]
        return resp

    def query_nlg(self, text, sender='isyatirim_test_default'):
        
        if text == '':
            return {'intent':{'name':'EMPTY TEXT','confidence':0.0}}
        if not isinstance(text, str):
            return {'intent':{'name':'NOT TEXT','confidence':0.0}}

        data = {"message": text, "sender":sender, "lang":"tr"}   
        data = json.dumps(data)
        resp = requests.post(self.nlg_url, data = data, verify=False )
        return resp.json() 

class DucklingAPI:

    def __init__(self, url='http://51.124.94.195:8000/parse', locale='tr_TR'):
        self.url = url
        self.locale = locale

    def query(self, text):
        if text == '':
            return {'intent':{'name':'EMPTY TEXT','confidence':0.0}}
        if not isinstance(text, str):
            return {'intent':{'name':'NOT TEXT','confidence':0.0}}
        
        data = {"text": text, "locale":self.locale}
        resp = requests.post(self.url, data = data, verify=False, )

        return resp.json()

    def minified_query(self, text, filters=None):
        resp = self.query(text)

        if filters and isinstance(filters,list):
            resp = [e for e in resp if e['dim'] in filters]

        resp = [{'body':e['body'], 'value':e['value'], 'dim':e['dim']} for e in resp]
        
        def minify_func(e):
            try:
                if e['dim'] in ['time']:
                    return {'body':e['body'], 'value':e['value']['value'], 'grain':e['value']['grain'], 'dim':e['dim']}
                elif e['dim'] in ['duration',]:
                    return {'body':e['body'], 'value':e['value']['value'], 'unit':e['value']['unit'], 'dim':e['dim']}
                else:
                    return e
            except:
                return e
        resp = [minify_func(e) for e in resp ]
        return resp

class STNLPAPI:
    def __init__(self, url='http://127.0.0.1:5005/model/parse'):
        self.url = url

    def query(self, text,):
        if text == '':
            return {'intent':{'name':'EMPTY TEXT','confidence':0.0}}
        if not isinstance(text, str):
            return {'intent':{'name':'NOT TEXT','confidence':0.0}}

        resp = requests.get(f'{self.url}?text={text}&bot_name=maxi', verify=False )
        return resp.json()

class FinieAPI:
    
    def __init__(self, url='https://finieservices.uatisbank/'):
        self.url = url
        self.session = requests.Session()
        self.session.verify = False
        
        self.data = {
            "query": "",
            "lat": "",
            "lon": "",
            "inputtype": "",
            "time_offset": 300,
            "classifier": "stateful-isbank-states-state",
            "dialog": "finie_session_start",
            "device": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36"
        }
        
        self.login()
    
    def login(self,):
        
        url = f'{self.url}v1/oauth/'
        params = "client_id=rKVJ1uEgfviTOc4BfXC5CyUgJD9VYxsvtyJxiCrT&client_secret=tvYCuNq2mB5xLgKChkSyehFA83YjIfqbmYZNYGDkcLUyw6BKITDRKQjiT5N7ynexNPbHc2UoMI2VosYtwLzT3CCL5MjAMaFX2k6wm8pGYS5JPcLo4Mew6jIQi1edLqHr&grant_type=client_credentials&clinc_user_id=161215276"
        data = dict([p.split('=') for p in params.split('&')])
        # resp = requests.post(url, data = data, verify=False )
        resp = self.session.post(url, data = data)
        self.access_token = resp.json()['access_token']
        self.session.headers.update(
            {
                'Authorization': f'Bearer {self.access_token}',
                'Accept': 'application/json'
            }
        )
        
        print(f'Login {resp.status_code} {self.access_token}')
        
        
    def query(self, text):
        url = f'{self.url}v1/query/'
        self.data['query'] = text
        resp =  self.session.post(url, json=self.data).json()

        if resp in [{'detail': 'Using expired access token.'},
                    {'detail': 'No such access token.'}]:
            print(resp['detail'])
            self.login()
            print('new token is obtained.')
            return self.query(text)
        else:
            return resp

class DoccanoClient:
    
    def get(self, endpoint: str, data: dict = {}, files: dict = {}, ):
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.get(request_url)

    
    def delete(self, endpoint: str, data: dict = {}, files: dict = {},):
        request_url = urljoin(self.baseurl, endpoint)
        if data:
            docs = data['results']

            for doc in docs:
                resp = self.session.delete(request_url+'/'+str(doc['id']))
                assert resp.status_code == 204
            
            return resp

        else:
            return self.session.delete(request_url)

    def post(self,endpoint: str,data: dict = {},files: dict = {},):
        request_url = urljoin(self.baseurl, endpoint)
        return self.session.post(request_url, data=data, files=files) #, verify=False )

    ####################################################################################
    ####################################################################################
    ####################################################################################

    def __init__(self, baseurl: str, username: str, password: str):
        self.baseurl = baseurl if baseurl[-1] == '/' else baseurl+'/'
        self.session = requests.Session()
        self.session.verify = False
        self._login(username, password)


        try:
            from spacy.lang.tr import Turkish as SpacyTurkish
            self.nlp = SpacyTurkish()
        except:
            pass



    def _login(
        self,
        username: str,
        password: str
    ) -> requests.models.Response:
        """
        Authorizes the DoccanoClient instance.

        Args:


        Returns:
            requests.models.Response: The authorization request response.
        """
        url = 'v1/auth-token'
        auth = {'username': username, 'password': password}
        response = self.post(url, auth)#, verify=False)
        print(response)
        token = response.json()['token']
        self.session.headers.update(
            {
                'Authorization': 'Token {token}'.format(token=token),
                'Accept': 'application/json'
            }
        )
        return response

    ###########################################################################
    ###########################################################################

    def generate_delete_data(self, config):
        
        data_config = config[1][-1]


        data = {}
        files = {}

        if data_config[0] == 'doc':
            if type(data_config[1]) == type({}):
                
                if 'results' in data_config[1]: # multiple doc data
                    data = data_config[1]

                    assert config[1][0][0] == 'project'
                    assert config[1][0][1] == data['source_project'] 
                    
        return data, files

    def generate_post_data(self, config):

        data_config = config[1][-1]


        data = {}
        files = {}
        
        if data_config[0] == 'project':

            assert 'name' in data_config[1]
            assert 'type' in data_config[1]

            project_type = data_config[1]['type']

            mapping = {'SequenceLabeling': 'SequenceLabelingProject',
                    'DocumentClassification': 'TextClassificationProject',
                    'Seq2seq': 'Seq2seqProject'}
            data = {
                'project_type': project_type,
                'description': 'no description',
                'guideline': 'no guideline',
                'resourcetype': mapping[project_type]
            }

            data.update(data_config[1])
            
        elif data_config[0] == 'doc':

            if type(data_config[1]) == type({}):
                
                if 'results' in data_config[1]: # multiple doc data
                    
                    upload_dump = self.project_docs_json_upload_dump(data_config[1])
                    
                    data = {'file': ('doccano.jsonl', upload_dump,),'format': 'json'}
                    files = {'file': ('doccano.jsonl',upload_dump,)}

                else: # single doc data
                    data = {
                        
                    }
                    
                    data.update(data_config[1])

            elif type(data_config[1]) == type([]):

                if str(type(data_config[1][0])) == "<class 'spacy.tokens.doc.Doc'>":
                    
                    upload_dump = self.spacy_docs_upload_dump(data_config[1])
                    data = {'file': ('doccano.jsonl', upload_dump,),'format': 'json'}
                    files = {'file': ('doccano.jsonl',upload_dump,)}

        else: # single data
            data = {
                
            }
            
            data.update(data_config[1])


        return data, files

    def generate_rest_endpoint(self, config):

        endpoint_config = config[1]

        # endpoint_config
        # # (('project', {'name':'test_v6', 'type':'SequenceLabeling'}),)
        # # (('project',13), ('doc',-1))

        object_mapping = {
            'user': 'users',
            'project': 'projects',
            'doc': 'docs',
            'role': 'roles',
            'label': 'labels',
            'ann': 'annotations',

            'statistics': 'statistics',
        }

        endpoint = 'v1'

        for idx, i in enumerate(endpoint_config):
            endpoint += '/' + object_mapping[i[0]] 

            if type(i[1]) == type(1): # GET REQUEST

                if i[1] == -1 and config[0] == 'get': # get all data                    
                    if i[0] == 'doc':
                        endpoint += '?limit=100000&offset=0'
                    assert idx == len(endpoint_config) - 1 # no other additions if value is -1
                else: # specify id of target data
                    endpoint += '/' + str(i[1])

            else: # POST, DELETE REQUESTS WITH DATA

                assert idx == len(endpoint_config) - 1 # no other additions if value is not integer
                
                if i[0] == 'doc':
                    if config[0] == 'post':
                        if type(i[1]) == type({}):
                            if 'results' in i[1]:
                                # multiple doc data upload
                                endpoint += '/upload' 
                        elif type(i[1]) == type([]):
                            if str(type(i[1][0])) == "<class 'spacy.tokens.doc.Doc'>":
                                # multiple doc data upload
                                endpoint += '/upload' 
                    elif config[0] == 'delete':
                        pass
                            

        return endpoint

    ###########################################################################
    ###########################################################################

    def update_doc_json(self, doc_json):
        doc_json = copy.deepcopy(doc_json)
        for item in doc_json['results']:
            if eval(item['meta']) == '{}':
                item['meta'] = eval(item['meta']) 
            item['meta'] = eval(item['meta'])
        return doc_json

    ###########################################################################
    ###########################################################################

    def project_docs_to_spacy(self, project_docs):

        plabels = self.rest_api(('get', (('project', project_docs['source_project']), ('label', -1)) ) ).json()
        plabels_id_to_text = {l['id']:l['text'] for l in plabels}
        
        docs = sorted(project_docs['results'], key=lambda x: x['id'] )
        
        results = []
        for doc in docs:
            results.append(self.project_doc_to_spacy(doc, plabels_id_to_text) )
        return results

    def project_doc_to_spacy(self, doc, plabels_id_to_text):
        
        from spacy.tokens import Token, Span
        from spacy.tokens.doc import Doc
        ###########################################################################
        doci = doc
        
        annotations = sorted(doci['annotations'], key=lambda x:x['start_offset']) # lambda x:x['id'] does not work
        tokens = [doci['text'][ann['start_offset']:ann['end_offset']] for ann in annotations]
        spaces = [annotations[i]['end_offset'] != annotations[i+1]['start_offset'] for i in range(0, len(tokens)-1)] + [False]

        sdoc = Doc(self.nlp.vocab, words=tokens, spaces=spaces)
        for idx, ann in enumerate(annotations):
            sdoc.ents += (Span(sdoc, idx, idx+1, label=plabels_id_to_text[ann['label']]), )

        
        if doci['text'] not in [' '.join(tokens), sdoc.text] :
            
            print(sdoc.text)
            print(doci['text'])
            print(' '.join(tokens))
            print(annotations)
            print()
        
        if [(ann['start_offset'],ann['end_offset']) for ann in annotations] !=  [(t.idx, t.idx+len(t.text)) for t in sdoc]:
            
            print(doci['text'])
            print(' '.join(tokens))
            print(annotations)
            print()

        # assert doci['text'] == ' '.join(tokens)
        # assert [(ann['start_offset'],ann['end_offset']) for ann in annotations] !=  [(t.idx, t.idx+len(t.text)) for t in sdoc]

        return sdoc

    def spacy_to_project_docs(self, project_docs, spacy_docs):

        project_docs = copy.deepcopy(project_docs)

        plabels = self.rest_api(('get', (('project', project_docs['source_project']), ('label', -1)) ) ).json()
        plabels_id_to_text = {l['id']:l['text'] for l in plabels}
        plabels_text_to_id = {l['text']:l['id'] for l in plabels}
        ## TODO if t.ent_type_ is not in plabels_text_to_id, a new label, it will raise error.

        project_docs['results'] = [{
            'text':sdoc.text, # sdoc.text.strip()
            'meta':{},
            'annotations':[{
                "start_offset": t.idx, 
                "end_offset": t.idx+len(t.text), 
                "label": plabels_text_to_id[t.ent_type_] } 
                for t in sdoc]} 
            for sdoc in spacy_docs]

        return project_docs

    def spacy_docs_upload_dump(self, spacy_docs):

        results = [{
                    'text': sdoc.text, # sdoc.text.strip()
                    'meta': {'0':'no meta'},
                    'labels':[[t.idx, t.idx+len(t.text), t.ent_type_ ] 
                        for t in sdoc]
                    } 
                for sdoc in spacy_docs]

        return '\n'.join([json.dumps(d) for d in results])

    def project_docs_json_upload_dump(self, project_docs):

        plabels = self.rest_api(('get', (('project', project_docs['source_project']), ('label', -1)) ) ).json()
        plabels_id_to_text = {l['id']:l['text'] for l in plabels}

        return '\n'.join([self.project_doc_json_upload_dump(doc_json, plabels_id_to_text) for doc_json in project_docs['results'] ])

    def project_doc_json_upload_dump(self, doc_json, plabels_id_to_text):
        json_doc = doc_json
        plabels = plabels_id_to_text
        
        json_doc = copy.deepcopy(json_doc)
        labels = [[ l['start_offset'], l['end_offset'], plabels[l['label']] ] for l in json_doc['annotations']]
        
        json_doc['labels'] = labels
        del json_doc['annotations']
        
        json_doc['meta'] =  {'0':'no meta'} if json_doc['meta'] == '{}' else json_doc['meta']
        
        json_dump = json.dumps(json_doc)
        return json_dump

    ###########################################################################
    ###########################################################################

    def backup_project(self, project_id, verbose=1):

        project = self.rest_api(('get', (('project', project_id), ) )).json() # id, name, description, project_type
        backup_project_name = project['name'] + '__backup__' + datetime.datetime.now().strftime('%Y%m%d__%H%M')
        
        ################################################
        if verbose == 1:
            print('  > creating new backup project')
        ################################################
        
        backup_project = self.rest_api(('post', (('project', {'name':backup_project_name, 'type':project['project_type']}),) )).json() # id, name, description, project_type
        backup_project_id = backup_project['id']
        
        ################################################
        if verbose == 1:
            print('  > created new backup project', backup_project_id)
        ################################################
        
        ################################################
        if verbose == 1:
            print('  > uploading labels')
        ################################################
        
        plabels = self.rest_api(('get', (('project', project_id), ('label', -1)) )).json()
        temp_codes = []
        temp_names = []
        for l in plabels:
            temp = self.rest_api(('post', (('project', backup_project_id), ('label', l)) ))
            temp_codes.append(temp.status_code)
            temp_names.append(temp.json()['text'])
        ################################################
        if verbose == 1:
            print('    > ',list(set(temp_codes)), temp_names)
        ################################################
        
        
        ################################################
        if verbose == 1:
            print('  > uploading documents')
        ################################################
        project_docs = self.rest_api(('get', (('project', project_id), ('doc', -1)) ))
        temp = self.rest_api(('post', (('project', backup_project_id), ('doc', project_docs)) ))
        
        ################################################
        if verbose == 1:
            print('  > uploaded documents', temp)
        ################################################
        pass

    def create_project_with_docs(self, project_name, project_type, docs, verbose=1):
        
        
        ################################################
        if verbose == 1:
            print('  > creating new project')
        ################################################

        new_project = self.rest_api(('post', (('project', {'name':project_name, 'type':project_type}),) )).json() # id, name, description, project_type
        new_project_id = new_project['id']

        ################################################
        if verbose == 1:
            print('  > created new project', new_project_id)
        ################################################

        ################################################
        if verbose == 1:
            print('  > uploading documents')
        ################################################

        temp = self.rest_api(('post', (('project', new_project_id), ('doc', docs) )) )

        ################################################
        if verbose == 1:
            print('  > uploaded documents', temp)
        ################################################
        pass

    ###########################################################################
    ###########################################################################

    def rest_api(self, config=(),):

        if "config notes":
            # config = ('get', (('project',-1),) )
            # config = ('get', (('project',13), ('label',14)) )
            # config = ('get', (('project',13), ('doc',-1)) )
            # config = ('get', {'project':13, 'doc':-1} )
            # config = ('post', (('project', {'name':'test_v6', 'type':'SequenceLabeling'}),) )

            """
            v1/users
            v1/roles
            v1/projects

            v1/projects/{project_id}

            v1/projects/{project_id}/roles
            v1/projects/{project_id}/statistics
            v1/projects/{project_id}/labels
            v1/projects/{project_id}/labels/{label_id}

            v1/projects/{project_id}/docs?limit={limit}&offset={offset}
            v1/projects/{project_id}/docs/{doc_id}
            
            v1/projects/{project_id}/docs/{doc_id}/annotations
            v1/projects/{project_id}/docs/{doc_id}/annotations/{annotation_id}

            #################################################################

            v1/projects/{project_id}/docs/download?q={file_format}
            v1/projects/{project_id}/docs/upload
            v1/projects/{project_id}/docs/{doc_id}/approve-labels

            """
            pass

        #############################################################################
        
        rest_mapping = {
            'get': self.get,
            'post': self.post,
            # 'create': self.post,
            'delete': self.delete,
        }
        rest_function = rest_mapping[config[0]]
        
        #############################################################################

        endpoint = self.generate_rest_endpoint(config)

        if config[0] in ['post']:
            data, files = self.generate_post_data(config)
        elif config[0] in ['delete']:
            data, files = self.generate_delete_data(config)
        else: 
            data, files = ({},{})
        
        #############################################################################

        response = rest_function(endpoint, data, files)
        
        #############################################################################
        
        setattr(response,'additional_info', ())
        response.additional_info += (config,)
        response.additional_info += (endpoint,)
        response.additional_info += (data,)

        if not (response.status_code >= 200 and response.status_code <300):
            response.additional_info += ('code is not 2xx',)

        output = response

        if response.status_code >= 200 and response.status_code <300:
            if config[0] == 'get' and config[1][-1][0] == 'doc':
                output = self.update_doc_json(response.json())

                assert len(config[1]) == 2
                assert config[1][0][0] == 'project'

                output['source_project'] = config[1][0][1] 

        return output

    
    ###########################################################################

    def get_features(self) -> requests.models.Response:
        """
        Gets features.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/features')

    ###########################################################################

    def get_me(self) -> requests.models.Response:
        """
        Gets this account information.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/me')

    def get_user_list(self) -> requests.models.Response:
        """
        Gets user list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/users')


    ###########################################################################

    def get_roles(self) -> requests.models.Response:
        """
        Gets available Doccano user roles.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/roles')

    def get_rolemapping_list(
        self,
        project_id: int,
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/roles'.format(
                project_id=project_id
            )
        )

    def get_rolemapping_detail(
        self,
        project_id: int,
        rolemapping_id: int,
    ) -> requests.models.Response:
        """
        Currently broken!
        """
        return self.get(
            'v1/projets/{project_id}/roles/{rolemapping_id}'.format(
                project_id=project_id,
                rolemapping_id=rolemapping_id
            )
        )

    ###########################################################################

    def get_project_list(self) -> requests.models.Response:
        """
        Gets projects list.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/projects')

    def create_project(self, name, description, project_type):
        mapping = {'SequenceLabeling': 'SequenceLabelingProject',
                   'DocumentClassification': 'TextClassificationProject',
                   'Seq2seq': 'Seq2seqProject'}
        data = {
            'name': name,
            'project_type': project_type,
            'description': description,
            'guideline': 'Hello',
            'resourcetype': mapping[project_type]
        }
        
        return self.post('v1/projects',data=data)
    
    def delete_project(self, project_id: int):
        
        return self.delete(
            'v1/projects/{project_id}'.format(
                project_id=project_id
            )
        )

    def get_project(self, project_id: int) -> requests.models.Response:
        """
        Gets details of a specific project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/projects/{project_id}'.format(project_id=project_id))

    def get_project_statistics(self, project_id: int) -> requests.models.Response:
        """
        Gets project statistics.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get('v1/projects/{project_id}/statistics'.format(project_id=project_id))

    ###########################################################################


    def get_label_list(
        self,
        project_id: int
    ) -> requests.models.Response:
        """
        Gets a list of labels in a given project.

        Args:
            project_id (int): A project ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels'.format(
                project_id=project_id
            )
        )

    def get_label_detail(
        self,
        project_id: int,
        label_id: int
    ) -> requests.models.Response:
        """
        Gets details of a specific label.

        Args:
            project_id (int): A project ID to query.
            label_id (int): A label ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/labels/{label_id}'.format(
                project_id=project_id,
                label_id=label_id
            )
        )

    ###########################################################################

    
    def build_url_parameter(self,url_parameter: dict):
        
        return ''.join(['?', '&'.join(['&'.join(['='.join([tup[0], str(value)]) for value in tup[1]]) for tup in url_parameter.items()])])

    def get_document_list(
        self,
        project_id: int,
        url_parameters: dict = {}
    ) -> requests.models.Response:
        """
        Gets a list of documents in a project.

        Args:
            project_id (int):
            url_parameters (dict): `limit` and `offset`

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs{url_parameters}'.format(
                project_id=project_id,
                url_parameters=self.build_url_parameter(url_parameters)
            )
        )

    def get_document_detail(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        Gets details of a given document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_doc_download(
        self,
        project_id: int,
        file_format: str = 'json'
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/download?q={file_format}'.format(
                project_id=project_id,
                file_format=file_format
            )
        )

    def post_doc_upload(
        self,
        project_id: int,
        file_format: str,
        file_name: str,
        file_path: str = './',
    ) -> requests.models.Response:
        """
        Uploads a file to a Doccano project.

        Args:
            project_id (int): The project id number.
            file_format (str): The file format, ex: `plain`, `json`, or `conll`.
            file_name (str): The name of the file.
            file_path (str): The parent path of the file. Defaults to `./`.

        Returns:
            requests.models.Response: The request response.
        """
        files = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            )
        }
        data = {
            'file': (
                file_name,
                open(os.path.join(file_path, file_name), 'rb')
            ),
            'format': file_format
        }
        return self.post(
            'v1/projects/{project_id}/docs/upload'.format(
                project_id=project_id
            ),
            files=files,
            data=data
        )

    ###########################################################################

    def get_annotation_list(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        Gets a list of annotations in a given project and document.

        Args:
            project_id (int): A project ID to query.
            doc_id (int): A document ID to query.

        Returns:
            requests.models.Response: The request response.
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    def get_annotation_detail(
        self,
        project_id: int,
        doc_id: int,
        annotation_id: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs/{doc_id}/annotations/{annotation_id}'.format(
                project_id=project_id,
                doc_id=doc_id,
                annotation_id=annotation_id
            )
        )

    ###########################################################################

    def post_approve_labels(
        self,
        project_id: int,
        doc_id: int
    ) -> requests.models.Response:
        """
        """
        return self.post(
            'v1/projects/{project_id}/docs/{doc_id}/approve-labels'.format(
                project_id=project_id,
                doc_id=doc_id
            )
        )

    ###########################################################################

    def _get_any_endpoint(
        self,
        endpoint: str
    ) -> requests.models.Response:
        """
        """
        # project_id: int,
        # limit: int,
        # offset: int
        return self.get(endpoint)

    def exp_get_doc_list(
        self,
        project_id: int,
        limit: int,
        offset: int
    ) -> requests.models.Response:
        """
        """
        return self.get(
            'v1/projects/{project_id}/docs?limit={limit}&offset={offset}'.format(
                project_id=project_id,
                limit=limit,
                offset=offset
            )
        )

    def __notes():
        if "doccano api notes":
            # import requests
            # username = 'admin'
            # password = 'qwer1234'
            # baseurl = 'http://192.168.1.28:8000/'
            # ## 
            # session = requests.Session()
            # url = baseurl + 'v1/auth-token'
            # auth = {'username': username, 'password': password}
            # response = session.post(url, auth)
            # response.json()
            # ##
            # client = requests.Session()
            # url = baseurl + 'v1/auth-token'
            # # url = f"{self.entrypoint}/v1/auth-token"
            # login = {"username": username, "password": password}
            # response = client.post(url, json=login)
            # response.json()["token"]
            # # str(response)
            # # self.auth_headers = {"Authorization": "Token {}".format(api_token)}
            
            # ------------------------
            
            ### annotations are not created
            # for d in docs.json()['results'][:10]:
            #     resp = doccano_client.session.post(doccano_client.baseurl+'v1/projects/26/docs', json=d)
            #     print(resp, resp.json())

            ### single doc conversion for annotations to labels
            # doccano_client.project_doc_json_upload_dump(p14docs['results'][0], p14labels_id_to_text)

            ### legacy multiple doc data upload
            # upload_dump = doccano_client.project_docs_json_upload_dump(p14docs) # '\n'.join([json.dumps(d) for d in p14docs['results']])
            # data = {'file': ('doccano.jsonl', upload_dump,),'format': 'json'}
            # files = {'file': ('doccano.jsonl',upload_dump,)}
            # doccano_client.post('http://192.168.1.28:8000/v1/projects/31/docs/upload', data=data, files=files)
            
            pass

            # ```
            #     get_rolemapping_detail # Currently broken!
            #     _get_any_endpoint
            # ```

            # ----

            #
            # - Gets this account information.
            # ```
            # doccano_client.get_me().json()
            #
            #     {'id': 1,
            #      'username': 'admin',
            #      'first_name': '',
            #      'last_name': '',
            #      'email': 'admin@example.com',
            #      'is_superuser': True}
            # ```
            # - Gets features.
            # ```
            # doccano_client.get_features().json()
            #     {'cloud_upload': False}
            # ```
            # - Gets available Doccano user roles. 
            # ```
            # doccano_client.get_roles().json()
            #     [{'id': 1, 'name': 'project_admin'},
            #      {'id': 2, 'name': 'annotator'},
            #      {'id': 3, 'name': 'annotation_approver'}]
            # ```

            # - Gets user list.
            # ```
            # doccano_client.get_user_list().json()
            #     [{'id': 1,
            #       'username': 'admin',
            #       'first_name': '',
            #       'last_name': '',
            #       'email': 'admin@example.com',
            #       'is_superuser': True}]
            # ```

            # ---

            # ```
            #     get_project_detail(project_id: int)
            #     get_project_statistics(project_id: int)
            #     def get_rolemapping_list(project_id: int)
            #     get_label_list(project_id: int)
            #     get_label_detail(project_id: int, label_id: int)
            #     get_document_detail(project_id: int, doc_id: int)
            #     get_annotation_list(project_id: int, doc_id: int)
            #     get_annotation_detail(project_id: int, doc_id: int, annotation_id: int)
            #     post_approve_labels(project_id: int, doc_id: int)
            # ```

            # ---

            # ```
            # doccano_client.delete_project(19)
            #
            # projdocs = [json.loads(line) for line in 
            #       doccano_client.get_doc_download(project_id=13, file_format='json1').text.strip().split('\n')]
            # doccano_client.get_doc_download(13, 'json')
            # doccano_client._get_any_endpoint('v1/projects/13/docs?limit=100000&offset=0')
            #
            # doccano_client.post_doc_upload(14, 'json', 
            #                                'doccano_class_no_6_v4.jsonl', 
            #                                '../sahin_resources/datasets/finie/Isbank29042020/__annotation/')
            # ```

            # ---

            # - Gets projects list.
            # ```
            # doccano_client.get_project_list().json()
            #     [{'id': 2,
            #       'name': 'ner_extraction_class_no_5',
            #       'description': 'class_no_5',
            #       'guideline': 'Please write annotation guideline.',
            #       'users': [1],
            #       'current_users_role': {'is_project_admin': True,
            #        'is_annotator': False,
            #        'is_annotation_approver': False},
            #       'project_type': 'SequenceLabeling',
            #       'image': '/static/assets/images/cats/sequence_labeling.jpg',
            #       'updated_at': '2020-06-22T08:23:57.493935Z',
            #       'randomize_document_order': False,
            #       'collaborative_annotation': True,
            #       'single_class_classification': False,
            #       'resourcetype': 'SequenceLabelingProject'},
            # ```

            # - Gets a list of documents in a project.
            # ```
            #     url_parameters={'limit':("20",), "offset":("60",)}
            # ```
            # ```
            # doccano_client.get_document_list(project_id=13, url_parameters=url_parameters).json()
            #     {'count': 422,
            #      'next': 'http://192.168.1.28:8000/v1/projects/13/docs?limit=20&offset=80',
            #      'previous': 'http://192.168.1.28:8000/v1/projects/13/docs?limit=20&offset=40',
            #      'results': [{'id': 9660,
            #        'text': 'bu ay ne kadar kredi kartı borcum bulunmakta ?',
            #        'annotations': [{'id': 37739,
            #          'prob': 0.0,
            #          'label': 83,
            #          'start_offset': 0,
            #          'end_offset': 2,
            #          'user': 1,
            #          'document': 9660},
            # ```
            # ```
            # (Equivalent - exp_get_doc_list(project_id: int,limit: int,offset: int)   )
            # ```
            #

            # - Gets project data.
            # ```
            # file_format : json, json1
            # ```
            # ```
            # proj = [json.loads(line) for line in 
            #         doccano_client.get_doc_download(project_id=13, file_format='json').text.strip().split('\n')]
            # ```
            # ```
            #     [{'id': 9600,
            #       'text': 'Bu ay kredi kartı borcum var mı ?',
            #       'annotations': [{'label': 83, 'start_offset': 0, 'end_offset': 2, 'user': 1},
            #        {'label': 83, 'start_offset': 3, 'end_offset': 5, 'user': 1},
            #        {'label': 89, 'start_offset': 6, 'end_offset': 11, 'user': 1},
            #        {'label': 90, 'start_offset': 12, 'end_offset': 17, 'user': 1},
            #        {'label': 83, 'start_offset': 18, 'end_offset': 24, 'user': 1},
            #        {'label': 83, 'start_offset': 25, 'end_offset': 28, 'user': 1},
            #        {'label': 83, 'start_offset': 29, 'end_offset': 31, 'user': 1},
            #        {'label': 83, 'start_offset': 32, 'end_offset': 33, 'user': 1}],
            #       'meta': {},
            #       'annotation_approver': None},
            # ```

            # ---

            # - Upload json1 (jsonl) file.
            #
            # ```
            #     doccano_client.post_doc_upload(14, 'json', 
            #         'doccano_class_no_6_v4.jsonl', 
            #         '../sahin_resources/datasets/finie/Isbank29042020/__annotation/')
            #     doccano_client.post_doc_upload(project_id: int, file_format: 'json', 
            #         file_name, file_path ) # plain, json,conll
            # ```

            # ---

            # - `('delete', (('project', 13), ('doc', 9600)) ) `
            # - `('delete', (('project', 25),) ) `
            #
            #
            # - `('post', (('project',{'name':'test_v6', 'type':'SequenceLabeling'}),) ) `
            # - `('post', (('project', 26), ('doc', {'text': 'Bu ay kredi kartı borcum var mı ?',})`
            # - `('post', (('project',31), ('doc', p14docs)) )`
            #
            #
            # - `('get', (('project',-1),) )`
            # - `('get', (('project', 27), ('doc', -1)) ) `
            # - `('get', (('project', 14), ('label', -1)) )`
            #
            #
            # - `response.additional_info`

            pass

    def help(self,):
        response = ""
        response += """
            project_data = {
                'name': name,
                'project_type': project_type,
                'description': description,
                'guideline': 'Hello',
                'resourcetype': mapping[project_type]
            }

            doc_data = {'text': text}

            label_data = {
                'text': text,
                'background_color': next_color,
                'shortcut': next_short
            }


            annotation_data = {
                'start_offset': 0,
                'end_offset': 5,
                'label': label['id'],
                'prob': 0.8
            }
        """

        response += """
            # doccano_client.rest_api(('post', (('project',{'name':'test_v6', 'type':'SequenceLabeling'}),) )).json()

            # p14docs = doccano_client.rest_api(('get', (('project', 35), ('doc', -1)) ))
            # p14sdocs = doccano_client.project_docs_to_spacy(p14docs)

            # p14docs_updated = doccano_client.spacy_to_project_docs(p14docs, p14sdocs)

            # doccano_client.rest_api(('post', (('project',32), ('doc', p14docs_updated)) ))
            # doccano_client.rest_api(('post', (('project',36), ('doc', p14docs)) ))
            # doccano_client.rest_api(('post', (('project',36), ('doc', p14sdocs)) ))
        """

        response +="""
            ('delete', (('project', 13), ('doc', 9600)) )
            ('delete', (('project', 25),) )
            ('post', (('project',{'name':'test_v6', 'type':'SequenceLabeling'}),) )
            ('post', (('project', 26), ('doc', {'text': 'Bu ay kredi kartı borcum var mı ?',})
            ('post', (('project',31), ('doc', p14docs)) )
            ('get', (('project',-1),) )
            ('get', (('project', 27), ('doc', -1)) )
            ('get', (('project', 14), ('label', -1)) )
            
            response.additional_info
        """

        response +="""
            # created = doccano_client.rest_api(('post', (('project', {'name':'6_foreign_currency', 'type':'SequenceLabeling'}),) ))
            # response = doccano_client.rest_api(('post', (('project', 38), ('doc', currency_sdocs) )) )

            # doccano_client.create_project_with_docs('X_project_name', 'SequenceLabeling', currency_sdocs)
            # doccano_client.backup_project(38,1)

            pdocs = doccano_client.rest_api(('get', (('project', 35), ('doc', -1)) ))
            psdocs = doccano_client.project_docs_to_spacy(p14docs)
        """

        print(response)
        return response




