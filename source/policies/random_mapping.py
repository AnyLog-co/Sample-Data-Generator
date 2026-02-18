import json
from source.northbound.rest_calls import RestClient
from source.policies.mappings import BASE_POLICY

TOPIC = "rand-data"

def main(conn:RestClient|None=None):
    BASE_POLICY["mapping"]["id"] = TOPIC
    BASE_POLICY["mapping"]["schema"].update({
        "value": {
            "type": "float",
            "bring": "[value]"
        }
    })

    print(json.dumps(BASE_POLICY, indent=2))

if __name__ == "__main__":
    main()