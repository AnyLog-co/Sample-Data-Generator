import kafka
import support


def connect_kafka(servers:str, exception:bool=False)->kafka.producer.kafka.KafkaProducer:
    """
    Connect to Kafka producer
    :args:
        servers:str - producer server
        exception:bool - whether or not to print exceptions
    :params:
        producer:kafka.producer.kafka.KafkaProducer - connection to producer
    :return:
        producer
    """
    try:
        producer = kafka.KafkaProducer(bootstrap_servers=servers)
    except Exception as e:
        producer = None
        if exception is True:
            print(f'Failed to connect to producer {servers} (Error: {e})')


    return producer


def publish_data(producer:kafka.producer.kafka.KafkaProducer, topic:str, data:dict, dbms:str, table:str, exception:bool=False)->bool:
    """
    Publish data to Kafka
    :args:
        producer:kafka.producer.kafka.KafkaProducer - connection to producer
        topic:str - topic to publish against
        data:dict - either list or dict of data to send into MQTT broker
        dbms:str - logical database
        table:str - logical table name
        exception:bool - whether or not to print exceptions
    :params:
        status:bool
        payloads:list - converted data
        future:kafka.producer.future.FutureRecordMetadata - publish result
        record_metadata:kafka.producer.future.RecordMetadata
    :return:
        status
    """
    status = True
    payloads = support.payload_conversions(payloads=data, dbms=dbms, table=table)
    for message in payloads:
        try:
            encode_message = message.encode()
        except Exception as e:
            status = False
            if exception is True:
                print(f'Failed to encode {content} (Error: {e}')
        else:
            try:
                future = producer.send(topic, value=encode_message)
            except KafkaError as e:
                status = False
                if exception is True:
                    print(f'Failed to publish against topic {topic} (Error: {e})')
            else:
                try:
                    record_metadata = future.get(timeout=100)
                except KafkaError as e:
                    status = False
                    if exception is True:
                        print(f'Failed to record metadata (Error: {e})')
                else:
                    if not isinstance(record_metadata, kafka.producer.future.RecordMetadata):
                        status = False

    return status