import curlify, json
from tinksync.config import DEBUG_MODE


def _debug(response):
    """Prints the request and response for debugging purposes."""
    if DEBUG_MODE:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("--- Sent request ---")
        print(curlify.to_curl(response.request))

        print("--- Received response ---")
        print(json.dumps(response.json(), indent=2))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
