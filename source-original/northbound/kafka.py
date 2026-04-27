import json
from typing import List

from kafka import KafkaProducer
from kafka.errors import KafkaTimeoutError, NoBrokersAvailable

from source.northbound.error_codes import KAFKA_ERROR_CODES


class KafkaClient:
    """
    Kafka producer client wrapper for connecting, publishing, and disconnecting
    from a Kafka broker with structured error handling.

    Mirrors the interface of MqttClient for drop-in familiarity.
    """

    def __init__(self, host: str, port: int, user: str = None, password: str = None, timeout: int = 60):
        """
        Initialize Kafka producer and verify broker connectivity

        :args:
            host:str - Kafka broker hostname or IP
            port:int - Kafka broker port
            user:str - optional SASL username for authentication
            password:str - optional SASL password for authentication
            timeout:int - request/delivery timeout in seconds
        :params:
            self.producer:KafkaProducer - underlying kafka-python Producer instance
            self._connected:bool - connection state flag
        :return:
            None
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.timeout = timeout

        self.producer = None
        self._connected = False

        self.connect()

    # -------------------------
    # Callbacks
    # -------------------------

    def _on_send_success(self, record_metadata):
        """
        Internal callback triggered on successful message delivery

        :args:
            record_metadata:RecordMetadata - topic, partition, and offset of delivered message
        :params:
            None
        :return:
            None
        """
        pass  # Hook for subclasses or future logging

    def _on_send_error(self, exc):
        """
        Internal callback triggered on failed message delivery

        :args:
            exc:Exception - the exception raised during delivery
        :params:
            None
        :return:
            None
        """
        error_name = type(exc).__name__
        error_msg = KAFKA_ERROR_CODES.get(error_name, str(exc))
        raise Exception(
            f"Kafka delivery failed to {self.host}:{self.port} "
            f"({error_name} - {error_msg})"
        )

    # -------------------------
    # Connection Handling
    # -------------------------

    def connect(self):
        """
        Establish connection to Kafka broker by initialising the producer

        :args:
            None
        :params:
            self.producer:KafkaProducer - configured producer instance
            self._connected:bool - updated connection state
        :return:
            None
        """
        try:
            config = {
                "bootstrap_servers":  f"{self.host}:{self.port}",
                "value_serializer":   lambda v: v if isinstance(v, (bytes, bytearray)) else v.encode("utf-8"),
                "request_timeout_ms": self.timeout * 1000,
                "max_block_ms":       self.timeout * 1000,
            }

            if self.user and self.password:
                config.update({
                    "security_protocol":   "SASL_PLAINTEXT",
                    "sasl_mechanism":      "PLAIN",
                    "sasl_plain_username": self.user,
                    "sasl_plain_password": self.password,
                })

            self.producer = KafkaProducer(**config)
            self._connected = True

        except NoBrokersAvailable:
            raise Exception(
                f"Failed to connect to Kafka broker {self.host}:{self.port} "
                f"(NoBrokersAvailable - No brokers available)"
            )
        except Exception as error:
            raise Exception(
                f"Failed to connect to Kafka broker {self.host}:{self.port} "
                f"(Error: {error})"
            )

    def disconnect(self):
        """
        Flush pending messages and disconnect from Kafka broker

        :args:
            None
        :params:
            self.producer:KafkaProducer - active producer instance
            self._connected:bool - updated connection state
        :return:
            None
        """
        try:
            if self.producer and self._connected:
                self.producer.flush(timeout=self.timeout)
                self.producer.close(timeout=self.timeout)
                self._connected = False
                self.producer = None
        except Exception as error:
            raise Exception(
                f"Failed to disconnect from Kafka broker {self.host}:{self.port} "
                f"(Error: {error})"
            )

    # -------------------------
    # Publish
    # -------------------------

    def publish_data(self, topic: str, payload: str | dict | List[dict]):
        """
        Publish data to a specific Kafka topic

        :args:
            topic:str - Kafka topic name
            payload:str|dict|List[dict] - message content to publish
        :params:
            future:FutureRecordMetadata - async result of the produce call
        :return:
            None
        """
        try:
            if not self._connected:
                raise Exception("Kafka producer is not connected")

            if not isinstance(payload, (str, bytes, bytearray)):
                payload = json.dumps(payload)

            future = (
                self.producer
                .send(topic, value=payload)
                .add_callback(self._on_send_success)
                .add_errback(self._on_send_error)
            )

            # Block until delivery is confirmed or timeout is reached
            future.get(timeout=self.timeout)

        except KafkaTimeoutError:
            raise Exception(
                f"Failed to publish to topic '{topic}' "
                f"against {self.host}:{self.port} (KafkaTimeoutError - Request timed out)"
            )
        except Exception as error:
            raise Exception(
                f"Failed to publish to topic '{topic}' "
                f"against {self.host}:{self.port} (Error: {error})"
            )