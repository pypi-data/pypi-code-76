import requests
import json

from datetime import datetime


ENDPOINT_STAGE = 'http://stage.ventanillaunica.chaco.gov.ar'
ENDPOINT_PROD = 'https://gobiernodigital.chaco.gob.ar'

API_ENDPOINTS = {
	'get_token_via_authorization_code': '_endpointbase_/oauth/v2/token',
	'get_token_application': '_endpointbase_/oauth/v2/token',
	'get_persona_via_cuil': '_endpointbase_/api/v1/persona/cuil/_cuil_',
	'get_persona_via_token': '_endpointbase_/api/v1/persona'
}

class TGD()
	def __init__(self, mode_stage=True, client_id, client_secret, url_base, redirect_url):
		self.client_id = client_id
		self.client_secret = client_secret
		self.url_base = url_base
		self.redirect_url = redirect_url
		self.mode_stage = mode_stage

	def get_endpoint_base(self):
		if self.mode_stage:
			return ENDPOINT_STAGE
		return ENDPOINT_PROD

	def get_token_application(self):
		url = API_ENDPOINTS['get_token_application'].replace("_endpointbase_", self.get_endpoint_base())

		payload = (("grant_type", "client_credentials"), ("client_id", self.client_id), ('client_secret', self.client_secret))
		
		response = requests.get(url, headers={'Content-Type': 'application/json'}, params=payload)
		access_token, expires_in = None, None
		
		if response.status_code == 200:
			data = response.json()
			access_token = data['access_token']
			expires_in = data['expires_in']

		return access_token, expires_in

class TGD_OAUTH(TGD):
	def __init__(self, mode_stage=True, client_id, client_secret, url_base, redirect_url):
		super().__init__(mode_stage=mode_stage,client_id=client_id, client_secret=client_secret, url_base=url_base, redirect_url= redirect_url)

	def get_user_by_cuil(self, cuil):
		access_token, expires_in = self.get_token_application()
		url = API_ENDPOINTS['get_persona_via_cuil'].replace('_cuil_', cuil) 
		
		user = None
		message = None
		if access_token and expires_in:
			response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % access_token})

			if response.status_code == 200:
				data = response.json()
				user = {'cuil': data['cuitCuil'], 'apellidos': data['apellidos'], 'nombres': data['nombres'], 'id': data['id']}
			elif response.status_code == 403:
				data = response.json()
				message = data["message"]
			else:
				message = "Ha ocurrido un inconveniente, contáctese con el Adminstrador (CODE_ERROR: 10-01-01 L45[%s])" % response.status_code
				
		# message = "Usuario obtenido corectamente"
		# user = {'cuil': '20362069247', 'apellidos': 'IBANEZ', 'nombres': 'Lucas Sebastian', 'id': 123456}
		return user, message

	def get_token_via_authorization_code(self, code):
		url = API_ENDPOINTS['get_token_via_authorization_code'].replace("_endpointbase_", self.get_endpoint_base())

		payload = (
			("code", code), 
			("grant_type", "authorization_code"),
			("client_id", self.client_id), 
			('client_secret', self.client_secret),
			("redirect_uri", self.redirect_url)
		)
		
		response = requests.get(url, headers={'Content-Type': 'application/json'}, params=payload)
		access_token, expires_in, refresh_token = None, None, None
		
		if response.status_code == 200:
			data = response.json()
			access_token = data['access_token']
			expires_in = data['expires_in']
			refresh_token = data['refresh_token']

		return access_token, expires_in, refresh_token

	def get_persona_via_token(self, access_token):
		url = API_ENDPOINTS['get_persona_via_token'].replace("_endpointbase_", self.get_endpoint_base())
		response = requests.get(url, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % (access_token)})
		
		user, message = None, None
		if response.status_code == 200:
			data = response.json()
			email = None
			try:
				email = data['emails'][0]['email']
			except Exception:
				pass
			
			dni = None
			for documento in data.get("tiposDocumentoPersona", []):
				if documento["tipoDocumento"]["tipoDocumento"] == "DNI":
					dni = documento["numeroDocumento"]
					break
			fecha_nacimiento = None
			if data['fechaNacimiento']: # 2020-06-26T10:24:13-0300
				fecha_nacimiento = 	datetime.strptime(data['fechaNacimiento'], '%Y-%m-%dT%H:%M:%S%z')
			user = {'cuil': data['cuitCuil'], 
			        'apellidos': data['apellidos'], 
			        'nombres': data['nombres'], 
			        'id': data['id'],
			        'email': email,
			        'sexo': data['sexo'],
			        'fecha_nacimiento': fecha_nacimiento,
			        'dni': dni }

		return user, message


class ApiComunicaciones(TGD_OAUTH):
	def enviar_notificacion(self, asunto, plazo_dias, contenido, persona_envia, cuils=[], cuof="6-283-0", lectura_obligatoria=False):
		access_token, expires_in = self.get_token_application()
		url = API_ENDPOINTS['comunicaciones'].replace("_endpointbase_", self.get_endpoint_base())

		data = None
		status = False

		x = {
		    "cuof": cuof,
		    "asunto": asunto,
		    "contenido": contenido,
		    "plazoDias": plazo_dias,
		    "cuils": cuils,
		    "lecturaObligatoria": lectura_obligatoria,
		    "personaEnvia": persona_envia
		}
		if access_token and expires_in:
			response = requests.post(url, headers={'Content-Type': 'application/json', 'Authorization': 'Bearer %s' % access_token}, data=json.dumps(x))

			if response.status_code in [200, 201]:
				data = response.json()
				status = True
			else:
				try:
					data = response.json()
				except Exception as e:
					data = {"error": str(e)}
				
				
		return data, status