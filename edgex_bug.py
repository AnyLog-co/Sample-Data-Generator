import json
import requests

DATA = [{
    "id": "fb68440c-0dea-49be-b2b2-8e9003ab78c2",
    "pushed": 1656093207769,
    "device": "Random-Integer-Generator01",
    "created": 1656093207759,
    "modified": 1656093207771,
    "origin": 1656093207757297700,
    "readings": [{
      "id": "95fa6063-9c6d-4a31-8237-9732c51ec3f7",
      "created": 1656093207759,
      "origin": 1656093207757240800,
      "device": "Random-Integer-Generator01",
      "name": "RandomValue_Int16",
      "value": "-12830",
      "valueType": "Int16"
    }]
  },{
    "id": "fc9e9640-66c3-424a-b572-9bd81126fcf8",
    "pushed": 1656092947759,
    "device": "Random-Integer-Generator01",
    "created": 1656092947754,
    "modified": 1656092947761,
    "origin": 1656092947752393700,
    "readings": [{
        "id": "a6fec012-7cc0-4a3b-adf1-6e64952ae46f",
        "created": 1656092947754,
        "origin": 1656092947752350200,
        "device": "Random-Integer-Generator01",
        "name": "RandomValue_Int8",
        "value": "8",
        "valueType": "Int8"
    }]
  },{
    "id": "fcd6662c-893b-42c8-89eb-1d3963359256",
    "pushed": 1656092787767,
    "device": "Random-Integer-Generator01",
    "created": 1656092787757,
    "modified": 1656092787768,
    "origin": 1656092787752256300,
    "readings": [{
        "id": "28307823-8b07-42dd-8089-599e6cf339d4",
        "created": 1656092787757,
        "origin": 1656092787752201200,
        "device": "Random-Integer-Generator01",
        "name": "RandomValue_Int32",
        "value": "-1653714562",
        "valueType": "Int32"
      }]
  },{
    "id": "c6859ebe-a36a-4e59-9170-58606393a367",
    "pushed": 1656093207769,
    "device": "Random-String-Generator01",
    "created": 1656093207759,
    "modified": 1656093207771,
    "origin": 1656093207757297700,
    "readings": [{
      "id": "1b62de10-8a85-4f43-8de8-20368c4bc0a0",
      "created": 1656093207759,
      "origin": 1656093207757240800,
      "device": "Random-String-Generator01",
      "name": "RandomValue_String",
      "value": "asafklahlgk;h",
      "valueType": "String"
    }]
  },{
  "id": "ff2b6be0-890c-4e21-9bac-70bce9d27612",
  "pushed": 1656092885326,
  "device": "Modbus TCP test device",
  "created": 1656092885317,
  "modified": 1656092885327,
  "origin": 1656092885314563800,
  "readings": [{
      "id": "57a765d7-80ed-4dbc-b89a-866e35dda251",
      "created": 1656092885317,
      "origin": 1656092885313868000,
      "device": "Modbus TCP test device",
      "name": "Temperature",
      "value": "0.000000e+00",
      "valueType": "Float64",
      "floatEncoding": "eNotation"
    },{
        "id": "bde7a5c5-2d61-4f6f-98d8-93a7e2ce1316",
        "created": 1656092885317,
        "origin": 1656092885311935200,
        "device": "Modbus TCP test device",
        "name": "OperationMode",
        "value": "Cool",
        "valueType": "String"
  },{
        "id": "f2acb1fb-f785-4cf4-8c80-8b97ab7f6056",
        "created": 1656092885317,
        "origin": 1656092885312948700,
        "device": "Modbus TCP test device",
        "name": "FanSpeed",
        "value": "Low",
        "valueType": "String"
    }]
}]

def __send_data(data):
    header = {
        "command": "data",
        "topic": "test",
        'User-Agent': 'AnyLog/1.23',
        'Content-Type': 'text/plain'
    }
    try:
        r = requests.post('http://10.0.0.78:7849', headers=header, data=json.dumps(data))
    except Exception as e:
        print(f'Failed to execute POST (Error: {e})')
    else:
        if int(r.status_code) != 200:
            print(f'Failed to execute POST (Network Error: {r.status_code})')


def send_data():
    # send full data
    __send_data(data=DATA)


    for data in DATA:
        if len(data['readings']) == 1:
            __send_data(data=data)
        else:
            readings = data['readings']
            data['readings'] = []
            for reading in readings:
                data['readings'].append(reading)
                __send_data(data=data)
                data['readings'] = []


if __name__ == '__main__':
    send_data()