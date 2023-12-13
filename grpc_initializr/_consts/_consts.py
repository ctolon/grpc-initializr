from .._utils._conf_generator import _grpc_service_conf_generator as grpc_service_conf_generator 

class _Constants:
    GRPC_HOST="0.0.0.0"
    GRPC_PORT="45752"
    WORKER=20
    GRPC_SERVER_OPTS=[
        ('grpc.max_send_message_length', 100 * 1024 * 1024),
        ('grpc.max_receive_message_length', 100 * 1024 * 1024),
        ('grpc.service_config', grpc_service_conf_generator())
        ]
    LOGGER_NAME="gRPC_Logger"
    LOG_LEVEL="INFO"
    LOG_DATEFMT="%Y-%m-%d %H:%M:%S"
    LOG_FORMAT="[%(levelname)s] %(asctime)s - %(message)s"

    