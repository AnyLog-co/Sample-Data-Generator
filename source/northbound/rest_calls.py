import json
import requests
from source.northbound.error_codes import REST_EXCEPTION_CODES
from source.northbound.error_codes import HTTP_STATUS_CODES
from source.northbound.error_codes import REQUEST_EXCEPTION_MAP


class RestClient:
    def __init__(self, conn:str, auth:tuple=None, timeout:float=60):
        """
        Class to support cURL requests against the network
        :args:
            conn:str - base for URL
        :params:
            self.url - full connection path
            self.timeout:float - REST timeout
            self.auth:tuple - authentication infomration
        """
        self.url = f"http://{conn}" if not conn.startswith("http") else conn
        self.timeout = timeout
        self.auth = auth

    def _execute_command(self, method:str, headers:dict, payload=None)->requests.Request:
        """
        Execute cURL command against the URL
        :args:
            method:str - method to execute (PUT, POST, GET)
            headers:dict - REST headers
            payload:Any - content to publish into AnyLog / EdgeLake
        :param:
            response:requests.Requests - REST request response
        :raise:
            raise exception if fails, using the exception coes in `error_code.py`
        :return:
            response if successful
        """
        if (isinstance(payload, list) and isinstance(payload[0], dict)) or isinstance(payload, dict):
            payload = json.dumps(payload)
            if headers.get("Content-Type") == "application/json":
                headers["Content-Type"] = "text/plain"
        try:
            response = requests.request(method=method.upper(), url=self.url, headers=headers, auth=self.auth,
                                        timeout=self.timeout, data=payload)
            response.raise_for_status()
        except requests.exceptions.HTTPError as error:
            response = None

            status_code = error.response.status_code
            status_msg = HTTP_STATUS_CODES.get(status_code)
            if not status_msg:
                # fallback to first-digit mapping to REST_EXCEPTION_CODES
                first_digit = int(str(status_code)[0])
                status_msg = REST_EXCEPTION_CODES.get(first_digit, "Unknown REST error")

            error_msg = (
                f"Failed to execute {method.upper()} against {self.url} "
                f"(Network Error {status_code}: {status_msg} | Response: {error.response.text})"
            )
            raise requests.exceptions.HTTPError(error_msg, response=error.response) from error

        except Exception as error:
            # Any transport/network errors (ConnectionError, Timeout, etc.)
            response = None

            error_type = type(error).__name__
            error_code = REQUEST_EXCEPTION_MAP.get(error_type, 899)
            error_msg = REST_EXCEPTION_CODES.get(error_code, str(error))

            raise Exception(
                f"Failed to execute {method.upper()} against {self.url} "
                f"(Transport Error {error_code}: {error_msg})"
            ) from error

        return response

    def publish_data(self, headers:dict, payload, method:str="POST"):
        """
        Execute REST POST / PUT command to publish data against AnyLog / EdgeLake
        :args:
            headers:dict - REST headers
            payload: Any - content to publish into AnyLog / EdgeLake
            method:dict - format to publish data (PUT or POST)
        :return:
            response from   `_execute_command`
        """
        return self._execute_command(method=method.upper(), headers=headers, payload=payload)

    def get_data(self, headers:dict|None=None, raw_response:bool=False):
        """
        Execute REST GET command to get data from AnyLog / EdgeLake
        :args:
            headers:dict - REST headers
            raw_response:bool - return raw response rather than extract data
        :return:
            if raw_response - return response
            else - try to parse in JSON if fails return text format
        """
        response = self._execute_command(method="GET", headers=headers)
        if raw_response:
            return response

        try:
            return response.json()
        except Exception:
            return response.text





