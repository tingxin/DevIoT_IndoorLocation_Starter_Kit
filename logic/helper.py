__author__ = 'tingxxu'

from base64 import b64encode
import json
import time
import sys
import httplib
from httplib import *
import ssl

from DevIoTGateway.config import config

server = config["service"]["address"]
server_username = config["service"]["username"]
server_password = config["service"]["password"]
map_name = config["service"]["map_name"]
clients_api = config["service"]["api"]
authority = config["service"]["authority"].lower() == "true"

mapCoordinate = "mapCoordinate"
mapInfo = "mapInfo"


class ServiceHelper:

    @staticmethod
    def get_all_clients():
        if authority:
            service_response = ServiceHelper.get_https_json_response(server, clients_api, server_username, server_password)
        else:
            service_response = ServiceHelper.get_http_json_response(server, clients_api)
        if service_response["status"] is 200:
            data = service_response['data']
            if isinstance(data, list):
                return data
            elif data is not None:
                return data["Locations"]["entries"]
        return None


    @staticmethod
    def get_https_json_response(server_address, api, username, password):
        """
        Returns the response from the URL specified
        """
        try:
            # lib opener
            response = {}
            context = ssl._create_unverified_context()
            conn = HTTPSConnection(server_address, context=context)
            auth = str.encode("%s:%s" % (str(username), str(password)))
            user_and_pass = b64encode(auth).decode("ascii")
            headers = {'Authorization': 'Basic %s' % user_and_pass, "Accept": 'application/json'}
            conn.request('GET', str(api), headers=headers)
            res = conn.getresponse()
            bit_data = res.read()
            string_data = bit_data.decode(encoding='UTF-8')
            if len(string_data) > 0:
                response['data'] = json.loads(string_data)
            else:
                response['data'] = None
            response['status'] = 200
        except:
            print("--MseHelper get_json_response error:", sys.exc_info()[1])
            response['data'] = sys.exc_info()[1]
            response['status'] = 400

        return response

    @staticmethod
    def get_http_json_response(server_address, api):
        try:
            response = {}
            conn = HTTPConnection(server_address)
            headers = {"Accept": 'application/json'}
            conn.request("GET", api, headers=headers)
            res = conn.getresponse()
            bit_data = res.read()
            string_data = bit_data.decode(encoding='UTF-8')
            if len(string_data) > 0:
                response['data'] = json.loads(string_data)
            else:
                response['data'] = None
            response['status'] = 200
        except:
            print("--MseHelper get_json_response error:", sys.exc_info()[1])
            response['data'] = sys.exc_info()[1]
            response['status'] = 400

        return response

    @staticmethod
    def post_data_auth(server_address, api, data, user, password):
        try:
            conn = httplib.HTTPConnection(server_address)

            auth = str.encode("%s:%s" % (str(user), str(password)))
            user_and_pass = b64encode(auth).decode("ascii")
            headers = {'Authorization': 'Basic %s' % user_and_pass, "Accept": 'application/json', 'Content-Type': 'application/json'}
            conn.request("PUT", api, data, headers)
            response = conn.getresponse()
            print(response.status)
            return True
        except IOError as e:
            print(e)
            return False
        except:
            print("--MseHelper post_data_auth error:", sys.exc_info()[1])
            return False

    @staticmethod
    def delete_data_auth(server_address, api, user, password):
        try:
            conn = httplib.HTTPConnection(server_address)

            auth = str.encode("%s:%s" % (str(user), str(password)))
            user_and_pass = b64encode(auth).decode("ascii")
            headers = {'Authorization': 'Basic %s' % user_and_pass, "Accept": 'application/json', 'Content-Type': 'application/json'}
            conn.request("DELETE", api, None, headers)

            response = conn.getresponse()
            print(response.status)
            return True
        except IOError as e:
            print(e)
            return False
        except:
            print("--MseHelper delete_data_auth error:", sys.exc_info()[1])
            return False