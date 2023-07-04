import curlify, json


def _debug(response):
    """Prints the request and response for debugging purposes."""
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    print("--- Sent request ---")
    print(curlify.to_curl(response.request))

    print("--- Received response ---")
    print(json.dumps(response.json(), indent=2))
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
