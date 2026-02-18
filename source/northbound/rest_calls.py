import requests

class RestClient:
    def __init__(self, conn:str, auth:tuple=None, timeout:float=60):
        self.url = f"http://{conn}"
        self.auth = auth
        self.timeout = timeout

    def __execute_command(self, method:str, headers:dict, payload=None):
        try:
            response = requests.request(method=method.upper(), url=self.url, headers=headers, auth=self.auth,
                                        timeout=self.timeout, data=payload)
        except Exception as error:
            raise Exception(f"Failed to execute {method.upper()} against {self.url} (Error: {error})")
        return response

    def publish_data(self, headers:dict, payload, method:str="post"):
        return self.__execute_command(method=method.upper(), headers=headers, payload=payload)
        
    def get_data(self, headers:dict):
        response = self.__execute_command(method="GET", headers=headers, payload=None)

        try:
            return response.json()
        except Exception:
            return response.text



def get_file_content(url:str=None, timeout:float=30):
    response = None
    try:
        response = requests.get(url=url, timeout=timeout)
        response.raise_for_status()
    except Exception as error:
        raise Exception(f"Failed to get content from {url} (Error: {error})")

    return response