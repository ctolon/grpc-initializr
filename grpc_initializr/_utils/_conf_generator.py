import json
from typing import Dict, List

def _grpc_service_conf_generator(
    list_of_services : List[Dict[str, str]] = [{}],
    timeout="30.0s",
    maxAttempts=5,
    waitForReady=True,
    initialBackoff="0.1s",
    maxBackoff="10s",
    backoffMultiplier=2,
    retryableStatusCodes=["UNAVAILABLE"]
    ) -> str:
    """gRPC Service Configuration Generator function.
    
    References:
    - https://fuchsia.googlesource.com/third_party/grpc/+/HEAD/doc/service_config.md
    - https://www.retinadata.com/blog/configuring-grpc-retries/
    - https://stackoverflow.com/questions/73172112/configuring-retry-policy-for-grpc-request
    - https://stackoverflow.com/questions/75931312/retry-policy-for-python-grpcs
    - github.com/grpc/proposal/blob/master/A6-client-retries.md#retry-policy-capabilities
    - https://chromium.googlesource.com/external/github.com/grpc/grpc/+/HEAD/examples/python/debug/
    

    Args:
        list_of_services (List[Dict[str, str]]): List of {'service': 'pkg.svc'} definitions. Example: [{'service': {'inference.Prediction'}]. Defaults to [{}] and 
            it configures same service confs to all RPCs.
        timeout (str): Timeout. Defaults to '30.0s'
        maxAttempts (int, optional): maxAttempts. Defaults to 5.
        waitForReady (bool): waitForReady. Defaults to True.
        initialBackoff (str, optional): initialBackoff. Defaults to "0.1s".
        maxBackoff (str, optional): maxBackoff. Defaults to "10s".
        backoffMultiplier (int, optional): backoffMultiplier. Defaults to 2.
        retryableStatusCodes (list, optional): List of retryableStatusCodes. Defaults to ['UNAVAILABLE'].

    Returns:
        str: gRPC Service configuration.
    """
    
    return json.dumps(
    {
        "methodConfig": [
            {
                "name": list_of_services,
                "timeout": timeout,
                "waitForReady": waitForReady,
                "retryPolicy": {
                    "maxAttempts": maxAttempts,
                    "initialBackoff": initialBackoff,
                    "maxBackoff": maxBackoff,
                    "backoffMultiplier": backoffMultiplier,
                    "retryableStatusCodes": retryableStatusCodes,
                },
            }
        ]
    }
)