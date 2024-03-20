import kafka
from data_generator.support import serialize_data

def __connect_kafka(conn:str, username:str, password:str, exception:bool=False)->kafka.KafkaProducer:
    if username is not None and password is not None:
        try:
            return kafka.KafkaProducer(
                bootstrap_servers=conn,
                security_protocol=kafka.SASL_PLAINTEXT,
                sasl_mechanism='PLAIN',
                sasl_plain_username=username,
                sasl_plain_password=password,
            )
        except Exception as error:
            if exception is True:
                print(f"Failed to connect to kafka against {conn} (Error: {error})")
    else:
        try:
            return kafka.KafkaProducer(
                bootstrap_servers=conn
            )
        except Exception as error:
            if exception is True:
                print(f"Failed to connect to kafka against {conn} (Error: {error})")


def __disconnect_kafka(kafka_producer:kafka.KafkaProducer, conn:str, exception:bool=False):
    status = True
    try:
        kafka_producer.close()
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to disconnect from Kafka on {conn} (Error: {error})")
    return status

def __publish_payload(kafka_producer:kafka.KafkaProducer, payload:str, topic:str, conn:str, exception:bool=False):
    status = True
    try:
        kafka_producer.send(topic=topic, value=payload.encode('utf-8'))
    except Exception as error:
        status = False
        if exception is True:
            print(f"Failed to publish data against {conn} (Error: {str(error)})")
    return status

def publish_kafka(conn:str, payload:list, topic:str, auth:tuple=(), exception:bool=False):
    username = None
    password = None

    if auth != ():
        username, password = auth

    serialized_payload = serialize_data(payload=payload)
    kafka_producer = __connect_kafka(conn=conn, username=username, password=password)
    if kafka_producer is not None:
        status = __publish_payload(kafka_producer=kafka_producer, payload=serialized_payload, topic=topic, conn=conn, exception=exception)
        if status is True:
            __disconnect_kafka(kafka_producer=kafka_producer, conn=conn, exception=exception)





