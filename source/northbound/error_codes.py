"""
Dicts with error consistent error message to be used for REST and MQTT
"""
from kafka.errors import KafkaError

MQTT_ERROR_CODES = {
    -1: "MQTT_ERR_NO_CONN",
    1: "Connection Refused: Unacceptable protocol version",
    2: "Connection Refused: Identifier rejected",
    3: "Connection Refused: Server Unavailable",
    4: "Connection Refused: Bad username or password",
    5: "Connection Refused: Not authorized",
    7: "Connection Lost",
    16: "Malformed MQTT packet",
}

# CONFLUENT_KAFKA_ERROR_CODES = {
#     KafkaError._ALL_BROKERS_DOWN:        "All brokers are down",
#     KafkaError._AUTHENTICATION:          "Authentication failure",
#     KafkaError._BAD_MSG:                 "Malformed message",
#     KafkaError.UNKNOWN_TOPIC_OR_PART:    "Unknown topic or partition",
#     KafkaError.MSG_SIZE_TOO_LARGE:       "Message size too large",
#     KafkaError.TOPIC_AUTHORIZATION_FAILED: "Topic authorization failed",
#     KafkaError.BROKER_NOT_AVAILABLE:     "Broker not available",
#     KafkaError._TIMED_OUT:               "Request timed out",
#     KafkaError._TRANSPORT:               "Transport failure",
#     KafkaError._UNKNOWN_PARTITION:       "Unknown partition",
#     KafkaError._UNKNOWN_TOPIC:           "Unknown topic",
# }

KAFKA_ERROR_CODES = {
    "NoBrokersAvailable":           "No brokers available",
    "KafkaTimeoutError":            "Request timed out",
    "TopicAuthorizationFailed":     "Topic authorization failed",
    "MessageSizeTooLargeError":     "Message size too large",
    "UnknownTopicOrPartitionError": "Unknown topic or partition",
    "BrokerNotAvailableError":      "Broker not available",
    "AuthenticationFailedError":    "Authentication failure",
    "KafkaConnectionError":         "Connection to broker failed",
}



REST_EXCEPTION_CODES = {
    1:  "ConnectionError - Failed to establish a new connection",
    2:  "Timeout - The request timed out",
    3:  "TooManyRedirects - Too many redirects",
    4:  "SSLError - SSL certificate verification failed",
    5:  "ProxyError - Proxy connection failed",
    6:  "InvalidURL - Invalid URL format",
    7:  "MissingSchema - URL missing schema (http/https)",
    8:  "ChunkedEncodingError - Invalid chunked response",
}

HTTP_STATUS_CODES = {
    # --- Informational ---
    100: "Continue",
    101: "Switching Protocols",

    # --- Success ---
    200: "OK",
    201: "Created",
    202: "Accepted",
    204: "No Content",

    # --- Redirection ---
    300: "Multiple Choices",
    301: "Moved Permanently",
    302: "Found",
    304: "Not Modified",

    # --- Client Errors ---
    400: "Bad Request",
    401: "Unauthorized",
    403: "Forbidden",
    404: "Not Found",
    405: "Method Not Allowed",
    408: "Request Timeout",
    409: "Conflict",
    410: "Gone",
    415: "Unsupported Media Type",
    418: "I'm a teapot",
    422: "Unprocessable Entity",
    429: "Too Many Requests",

    # --- Server Errors ---
    500: "Internal Server Error",
    501: "Not Implemented",
    502: "Bad Gateway",
    503: "Service Unavailable",
    504: "Gateway Timeout",

    # --- Custom Extended Range ---
    600: "Network Connect Timeout Error",
    601: "DNS Resolution Failed",
    602: "Upstream Service Timeout",
    700: "Transport Layer Failure",
    800: "Application Layer Failure",
    899: "Unknown REST Error"
}

REQUEST_EXCEPTION_MAP = {
    "ConnectionError": 1,
    "Timeout": 2,
    "TooManyRedirects": 3,
    "SSLError": 4,
    "ProxyError": 5,
    "InvalidURL": 6,
    "MissingSchema": 7,
    "ChunkedEncodingError": 8,
}