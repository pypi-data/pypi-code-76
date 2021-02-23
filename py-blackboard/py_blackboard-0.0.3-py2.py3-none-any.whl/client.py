import jwt
import requests
from datetime import datetime, timedelta

APPLICATION_JSON = "application/json"
APPLICATION_FORM_URLENCODED = "application/x-www-form-urlencoded"

class BlackboardClient:
    """
    BlackboardClient class that handles all the blackboard requests.
    """
    url = None
    key = None
    secret = None
    jwt_duration = None
    session = None
    access_token = None

    def __init__(self, key: str, secret: str, url: str = "https://eu-lti.bbcollab.com/collab/api/csa", jwt_duration: int = 365):
        """
        initializes the blackboard client using the input parameters.

        :param key: blackboard client key
        :param secret: blackboard client secret
        :param url: blackboard api url
        :param jwt_duration: jwt token duration (in days)
        """
        self.key = key
        self.secret = secret
        self.url = url
        self.jwt_duration = jwt_duration
        # initialize the requests session
        self.session = requests.Session()
        # authenticate the session
        self.authenticate()

    def authenticate(self) -> None:
        """
        authenticates the client using the parameters passed during the initialization.
        """
        # create the jwt payload and encode the jwt
        jwt_exp = datetime.now() + timedelta(self.jwt_duration)
        jwt_payload = {
            "iss": self.key,
            "exp": jwt_exp.timestamp()
        }
        encoded_jwt = jwt.encode(jwt_payload, self.secret, algorithm="HS256")
        # send the auth request
        auth_res = self.session.post(
            "%s/token" % self.url,
            params={
                "grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": encoded_jwt
            },
            headers={"content-type": APPLICATION_FORM_URLENCODED}
        )
        # authenticate again.
        if auth_res.status_code == 200:
            auth_res = auth_res.json()
            self.access_token = auth_res.get('access_token')
            if not self.access_token:
                raise Exception("blackboard did not return any access token.")
            self.session.headers.update({"Authorization": "Bearer %s" % (self.access_token, )})
        if not self.access_token:
            raise Exception("blackboard did not return any access token.")

    ####################
    # contexts methods #
    ####################

    def get_contexts(self, params: dict = {}) -> dict:
        """
        retrieves all the contexts using the given parameters.

        :param params: query string that will be passed to the request.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/contexts" % (self.url, ),
            params=params,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_contexts] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))
  
    def create_context(self, context: dict) -> dict:
        """
        creates a new context using the input one.

        :param context: new context to create
        :returns: requests Response json object
        """
        res = self.session.post(
            "%s/contexts" % (self.url, ),
            json=context,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[create_context] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def update_context(self, context_id: str, data: dict) -> dict:
        """
        updates the context with the given context_id using the input data.

        :param context_id: id of the context to update.
        :param data: updated context data.
        :returns: requests Response json object
        """
        res = self.session.put(
            "%s/contexts/%s" % (self.url, context_id, ),
            json=data,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[update_context] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def delete_context(self, context_id: str) -> dict:
        """
        deletes the context with the given context_id.

        :param context_id: id of the context to delete.
        :returns: requests Response json object
        """
        res = self.session.delete(
            "%s/contexts/%s" % (self.url, context_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[delete_context] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def associate_context_to_session(self, context_id: str, session_id: str) -> dict:
        """
        associates the given session to the given context.

        :param context_id: id of the context.
        :param session_id: id of the session to associate.
        :returns: requests Response json object
        """
        res = self.session.post(
            "%s/contexts/%s/sessions" % (self.url, context_id ),
            json={ "id": session_id },
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[associate_context_to_session] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    ######################
    # recordings methods #
    ######################

    def get_recordings(self, params: dict = {}) -> dict:
        """
        retrieves all the recordings using the given parameters.

        :param params: query string that will be passed to the request.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/recordings" % (self.url, ),
            params=params,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_recordings] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_recording_list(self, recording_id: str) -> dict:
        """
        retrieves the recording list for the recording with the given id.

        :param recording_id: id of the recording.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/recordings/list" % (self.url, ),
            params={"id": recording_id},
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_recording_list] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def delete_recording(self, recording_id: str) -> dict:
        """
        deletes the recording with the given id.

        :param recording_id: id of the recording.
        :returns: requests Response json object
        """

        res = self.session.delete(
            "%s/recordings/%s" % (self.url, recording_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[delete_recording] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    ####################
    # sessions methods #
    ####################

    def get_sessions(self, params: dict = {}) -> dict:
        """
        retrieves all the sessions using the given parameters.

        :param params: query string that will be passed to the request.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/sessions" % (self.url, ),
            params=params,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_sessions] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_by_id(self, session_id: str) -> dict:
        """
        retrieves the session with the given session_id.

        :param session_id: id of the user to retrieve.
        :returns: tuple ()(requests Response json object, error)
        """
        res = self.session.get(
            "%s/sessions/%s" % (self.url, session_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_by_id] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))


    def get_session_by_external_id(self, session_external_id: str) -> dict:
        """
        retrieves the session with the given session_external_id.

        :param session_external_id: external id of the session to retrieve.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/sessions" % (self.url, ),
            params={"extId": session_external_id},
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_by_external_id] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def create_session(self, session: dict) -> dict:
        """
        creates a new session using the input one.

        :param session: new session to create
        :returns: requests Response json object
        """
        res = self.session.post(
            "%s/sessions" % (self.url, ),
            json=session,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[create_session] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def update_session(self, session_id: str, data: dict) -> dict:
        """
        updates the session with the given session_id using the input data.

        :param session_id: id of the session to update.
        :param data: updated session data.
        :returns: requests Response json object
        """
        res = self.session.put(
            "%s/sessions/%s" % (self.url, session_id, ),
            json=data,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[update_session] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def delete_session(self, session_id: str) -> dict:
        """
        deletes the session with the given session_id.

        :param session_id: id of the session to delete.
        :returns: requests Response json object
        """
        res = self.session.delete(
            "%s/sessions/%s" % (self.url, session_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[delete_session] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    #######################
    # enrollments methods #
    #######################

    def enroll_user(self, session_id: str, user_id: str, launching_role: str = "moderator", editing_permission: str = "writer") -> dict:
        """
        enrolls the user with the given user_id in the session with the given session_id.

        :param session_id: id of the session where the user will be enrolled.
        :param session_id: id of the user that will be enrolled.
        :returns: requests Response json object
        """
        res = self.session.post(
            "%s/sessions/%s/enrollments" % (self.url, session_id, ),
            json={
                "userId": user_id,
                "launchingRole": launching_role,
                "editingPermission": editing_permission
            },
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[enroll_user] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_enrollment(self, session_id: str, enrollment_id: str) -> dict:
        """
        returns the enrollment with the given enrollment_id for the session with the given session_id.

        :param session_id: id of the session where to search for the enrollment.
        :param enrollment: id of the enrollment to find.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/sessions/%s/enrollments/%s" % (self.url, session_id, enrollment_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_enrollment] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def delete_session_enrollment(self, session_id: str, enrollment_id: str) -> dict:
        """
        deletes the enrollment with the given enrollment_id for the session with the given session_id.

        :param session_id: id of the session where to delete the enrollment.
        :param enrollment: id of the enrollment to delete.
        :returns: requests Response json object
        """
        res = self.session.delete(
            "%s/sessions/%s/enrollments/%s" % (self.url, session_id, enrollment_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_enrollment] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_enrollments(self, session_id: str, params: dict = {}) -> dict:
        """
        retrieves all the enrollments for the session with the given session_id.

        :param session_id: id of the session where to retrieve the enrollments.
        :param params: query string that will be passed to the request.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/sessions/%s/enrollments" % (self.url, session_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_enrollments] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_enrollment_url(self, session_id: str, enrollment_id: str) -> dict:
        """
        returns the launch URL for enrollment passed as input.

        :param session_id: id of the session where to retrieve the enrollment.
        :param enrollment_id: id of the enrollment where to retrieve the launch URL.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/sessions/%s/enrollments/%s/url" % (self.url, session_id, enrollment_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_enrollment_url] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))


    #####################
    # instances methods #
    #####################

    def get_session_instances(self, session_id: str, params: dict = {}) -> dict:
        """
        retrieves all the session instances for the session with the given session_id.

        :param session_id: id of the session where to retrieve the instances.
        :param params: query string that will be passed to the request.
        :returns: requests Response json object.
        """
        res = self.session.get(
            "%s/sessions/%s/instances" % (self.url, session_id),
            headers={"content-type": APPLICATION_JSON},
            params=params
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_instances] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_instance_stats(self, session_id: str, instance_id: str) -> dict:
        """
        retrieves all the attendance stats for the given session instance.

        :param session_id: id of the session where to retrieve the instance.
        :param instance_id: id of the instance where to retrieve the stats.
        :returns: requests Response json object.
        """
        res = self.session.get(
            "%s/sessions/%s/instances/%s/stats" % (self.url, session_id, instance_id),
            headers={"content-type": APPLICATION_JSON},
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_instance_stats] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_session_instance_attendees(self, session_id: str, instance_id: str) -> dict:
        """
        retrieves all the attendance attendees for the given session instance.

        :param session_id: id of the session where to retrieve the instance.
        :param instance_id: id of the instance where to retrieve the attendees.
        :returns: requests Response json object.
        """
        res = self.session.get(
            "%s/sessions/%s/instances/%s/attendees" % (self.url, session_id, instance_id),
            headers={"content-type": APPLICATION_JSON},
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_session_instance_attendees] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))


    #################
    # users methods #
    #################

    def get_users(self, params: dict = {}) -> dict:
        """
        retrieves all the users using the given parameters.

        :param params: query string that will be passed to the request.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/users" % (self.url, ),
            params=params,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_users] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_user_by_id(self, user_id: str) -> dict:
        """
        retrieves the user with the given user_id.

        :param user_id: id of the user to retrieve.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/users/%s" % (self.url, user_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_user_by_id] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def get_user_by_external_id(self, user_external_id: str) -> dict:
        """
        retrieves the user with the given user_external_id.

        :param user_external_id: external id of the user to retrieve.
        :returns: requests Response json object
        """
        res = self.session.get(
            "%s/users" % (self.url, ),
            params={"extId": user_external_id},
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[get_user_by_external_id] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))


    def create_user(self, user: dict) -> dict:
        """
        creates a new user using the input one.

        :param user: new user to create
        :returns: requests Response json object
        """
        res = self.session.post(
            "%s/users" % (self.url, ),
            json=user,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[create_user] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def update_user(self, user_id: str, data: dict) -> dict:
        """
        updates the user with the given user_id using the input data.

        :param user_id: id of the user to update.
        :param data: updated user data.
        :returns: requests Response json object
        """
        res = self.session.put(
            "%s/users/%s" % (self.url, user_id, ),
            json=data,
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[update_user] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))

    def delete_user(self, user_id: str) -> dict:
        """
        deletes the user with the given user_id.

        :param user_id: id of the user to delete.
        :returns: requests Response json object
        """
        res = self.session.delete(
            "%s/users/%s" % (self.url, user_id, ),
            headers={"content-type": APPLICATION_JSON}
        )
        if res.status_code == 200:
            return res.json()
        raise Exception("[delete_user] status code %d - error: %s" % (res.status_code, res.json().get("errorMessage", "unknown error occurred.")))