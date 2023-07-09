import curlify, json, os
DEBUG_MODE = os.environ.get("DEBUG_MODE") == "1"


def _debug(response):
    """Prints the request and response for debugging purposes."""
    if DEBUG_MODE:
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        print("--- Sent request ---")
        print(curlify.to_curl(response.request))

        print("--- Received response ---")
        print(json.dumps(response.json(), indent=2))
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
