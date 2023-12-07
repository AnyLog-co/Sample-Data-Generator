from src.support.__support__ import json_dumps

def print_results(payloads:list):
    """
    Print payloads one line at a time
    :args:
        payloads:list - list of payloads
    :return:
        print output per payload
    """
    for payload in payloads:
        print(json_dumps(payloads=payload, indent=None))


