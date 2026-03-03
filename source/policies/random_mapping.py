import json

from source.northbound.rest_calls import RestClient
from source.policies.mappings import BASE_POLICY
from source.northbound.rest_functions import declare_policy
from source.northbound.rest_functions import declare_msg_client

TOPIC = "rand-data"

def main(conn:RestClient|None, broker:str, port:int, is_rest:bool=False):
    BASE_POLICY["mapping"]["id"] = TOPIC
    BASE_POLICY["mapping"]["schema"].update({
        "value": {
            "type": "float",
            "bring": "[value]"
        }
    })

    policy_id = declare_policy(conn=conn, policy=BASE_POLICY)
    declare_msg_client(conn=conn, broker=broker, port=port, is_rest=is_rest,
                       topics=f"(name={TOPIC} and policy={policy_id})")

# if __name__ == "__main__":
#     main()