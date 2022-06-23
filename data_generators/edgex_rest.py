import requests
import time


def get_data(previous_count:int=0, exception:bool=False)->(int, list):
    """
    The following method extracts data from a local EdgeX
    :args:
        previous_count:str - total number of rows previously extracted
        exception:bool - whether or not to print exception
    :params:
        r:requests.get - GET request
        data:list - data from EdgeX
    :return:
        number of rows extracted &  list of data
    """
    try:
        r = requests.get('http://127.0.0.1:48080/api/v1/reading')
    except Exception as e:
        if exception is True:
            print(f'Failed to extract data from EdgeX (Error: {e})')
    else:
        try:
            data = r.json()
        except Exception as e:
            try:
                data = r.text
            except Exception as e:
                print(f'Failed to extract data from EdgeX (Error: {e})')
    if previous_count == 0:
        return len(data), data
    else:
        data = data[previous_count:]
        return len(data), data