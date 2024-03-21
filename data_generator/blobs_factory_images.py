def __get_data(file_name:str, exception:bool)->(list, str):
    """
    From JSON file extract status and detection fro a given file_name
    :args:
        file_name:str - file name to check against in the JSON
        exception:bool - whether to print exceptions to screen
    :params:
        output:dict - raw content from JSON file
        status:str - status value based on file_name
        detection:list - detection value(s) based on file_name
    :return:
        detection, status
    """
    output = None
    status = "Nok"
    detection = []
    try:
        with open(JSON_FILE, 'rb') as f:
            try:
                output = json.load(f)
            except Exception as error:
                if exception is True:
                    print(f"Failed to read content in {JSON_FILE} (Error: {error})")
    except Exception as error:
        if exception is True:
            print(f"Failed to open JSON file {JSON_FILE} (Error: {error})")

    if output is not None and file_name in output and "result" in output[file_name] and "detection" in output[file_name]["result"]:
        detection = output[file_name]["result"]["detection"]
    if output is not None and file_name in output and "status" in output[file_name]:
        status = output[file_name]["status"]

    return detection, status
