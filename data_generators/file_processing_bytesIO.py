import io
import os.path


def read_file(file_name:str, exception:bool=False)->(bool, io.BytesIO):
    status = True
    content = None

    if os.path.isfile(file_name):
        try:
            with open(file_name, "rb") as f:
                try:
                    content = io.BytesIO(f.read())
                except Exception as error:
                    status = False
                    if exception is True:
                        print(f"Failed to convert file content into byte format (Error: {error})")
        except Exception as error:
            status = False
            if exception is True:
                print(f"Failed to open {file_name} to be read (Error: {error})")
    else:
        print(f"Failed to locate {file_name}")

    return status, content


def extract_results(content:io.BytesIO, exception:bool=False)->str:
    try:
        output = content.read()
    except Exception as error:
        output = None
        if exception is True:
            print(f"Failed to read content from file (Error: {error})")

    return output


def main(file_name:str, exception:bool=False):
    status, content = read_file(file_name=file_name, exception=exception)
    return extract_results(content=content, exception=exception)