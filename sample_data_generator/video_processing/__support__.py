import numpy as np

def read_csv_to_dict(file_path):
    # Load the CSV file using numpy.genfromtxt
    data = np.genfromtxt(file_path, delimiter=',', dtype=None, names=True, encoding=None)

    # Convert the numpy array to a list of dictionaries
    data_dict_list = [{key: value for key, value in zip(data.dtype.names, row)} for row in data]

    # Convert the list of dictionaries to a single dictionary
    data_dict = {item['video']: item['count'] for item in data_dict_list}

    return data_dict
