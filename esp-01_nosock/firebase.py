"""
firebase Python package is a python interface to the Google's Firebase REST APIs
By Joe Tilsed
"""
import json
from parse import urlencode, quote
import requests as requests

name = 'firebase'

def author():
    return "Joe Tilsed - https://linkedin.com/in/JoeTilsed"

class Firebase(object):
    """ Firebase Interface """
    def __init__(self, config):
        self.api_key = config["apiKey"]
        self.auth_domain = config["authDomain"]
        self.database_url = config["databaseURL"]
        self.storage_bucket = config["storageBucket"]
        self.credentials = None
        self.requests = requests
    def auth(self):
        return Auth(self.api_key, self.requests, self.credentials)

    def database(self):
        return Database(self.credentials, self.api_key, self.database_url, self.requests)

class Auth:
    """ Authentication Service """
    def __init__(self, api_key, requests_session, credentials):
        self.api_key = api_key
        self.current_user = None
        self.requests = requests_session
        self.credentials = credentials

    def sign_in_with_email_and_password(self, email, password):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/verifyPassword?key={}".format(
            self.api_key
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"email": email, "password": password, "returnSecureToken": True})
        request_object = requests.post(request_ref, headers=headers, data=data)
        raise_detailed_error(request_object)
        self.current_user = request_object.json()
        return self.current_user

    def refresh(self, refresh_token):
        request_ref = "https://securetoken.googleapis.com/v1/token?key={}".format(self.api_key)
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"grantType": "refresh_token", "refreshToken": refresh_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        raise_detailed_error(request_object)
        request_object_json = request_object.json()
        return {
            "userId": request_object_json["user_id"],
            "idToken": request_object_json["id_token"],
            "refreshToken": request_object_json["refresh_token"]
        }

    def get_account_info(self, id_token):
        request_ref = "https://www.googleapis.com/identitytoolkit/v3/relyingparty/getAccountInfo?key={}".format(
            self.api_key
        )
        headers = {"content-type": "application/json; charset=UTF-8"}
        data = json.dumps({"idToken": id_token})
        request_object = requests.post(request_ref, headers=headers, data=data)
        raise_detailed_error(request_object)
        return request_object.json()

class Database:
    """ Database Service """
    def __init__(self, credentials, api_key, database_url, requests_session):

        if not database_url.endswith('/'):
            url = ''.join([database_url, '/'])
        else:
            url = database_url

        self.credentials = credentials
        self.api_key = api_key
        self.database_url = url
        self.requests = requests_session

        self.path = ""
        self.build_query = {}
        self.last_push_time = 0
        self.last_rand_chars = []

    def child(self, *args):
        new_path = "/".join([str(arg) for arg in args])
        if self.path:
            self.path += "/{}".format(new_path)
        else:
            if new_path.startswith("/"):
                new_path = new_path[1:]
            self.path = new_path
        return self

    def build_request_url(self, token):
        parameters = {}
        if token:
            parameters['auth'] = token
        for param in list(self.build_query):
            if type(self.build_query[param]) is str:
                parameters[param] = quote('"' + self.build_query[param] + '"')
            elif type(self.build_query[param]) is bool:
                parameters[param] = "true" if self.build_query[param] else "false"
            else:
                parameters[param] = self.build_query[param]
        request_ref = '{0}{1}.json?{2}'.format(self.database_url, self.path, urlencode(parameters))
        self.path = ""
        self.build_query = {}
        return request_ref

    def build_headers(self, token=None):
        headers = {"content-type": "application/json; charset=UTF-8"}
        if not token and self.credentials:
            access_token = self.credentials.get_access_token().access_token
            headers['Authorization'] = 'Bearer ' + access_token
        return headers

    def get(self, token=None, json_kwargs={}):
        request_ref = self.build_request_url(token)
        headers = self.build_headers(token)
        request_object = self.requests.get(request_ref, headers=headers)
        raise_detailed_error(request_object)
        request_dict = request_object.json(**json_kwargs)
        return request_dict

    def update(self, data, token=None, json_kwargs={}):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.patch(
            request_ref, headers=headers, data=json.dumps(data, **json_kwargs).encode("utf-8")
        )
        raise_detailed_error(request_object)
        return request_object.json()

    def remove(self, token=None):
        request_ref = self.check_token(self.database_url, self.path, token)
        self.path = ""
        headers = self.build_headers(token)
        request_object = self.requests.delete(request_ref, headers=headers)
        raise_detailed_error(request_object)
        return request_object.json()

    @staticmethod
    def check_token(database_url, path, token):
        if token:
            return '{0}{1}.json?auth={2}'.format(database_url, path, token)
        else:
            return '{0}{1}.json'.format(database_url, path)

def raise_detailed_error(request_object):
    try:
        pass
    except ValueError as e:
        raise ValueError(e, request_object.text)

