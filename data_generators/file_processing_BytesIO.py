import io
import os.path


def __read_file(file_name:str, exception:bool=False)->(bool, io.BytesIO):
    status = True
    content = None
    full_path = os.path.expanduser(os.path.expandvars(file_name))

    if os.path.isfile(full_path):
        try:
            with open(full_path, "rb") as f:
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


def main(file_name:str, exception:bool=False):
    bytesio_msg = None
    status, content = __read_file(file_name=file_name, exception=exception)
    print(content.read())



if __name__ == '__main__':
    main(file_name='$HOME/Downloads/sample_data/images/20200306202543226.jpeg', exception=True)