from urllib.parse import unquote
import logging
import json
import traceback

from google.protobuf.json_format import MessageToDict

import grpc

def _get_ip_port_from_context(context):
    peer = unquote(context.peer())
    ip = peer[peer.find(':')+1:peer.rfind(':')]
    port = peer[peer.rfind(':')+1:]
    return ip, port

def client_request_print(request, context, logger: logging.Logger) -> tuple:
    
    
    ip, port = _get_ip_port_from_context(context=context)
    
    try:
        request = MessageToDict(request, preserving_proto_field_name=True)
    except Exception as e:
        exc = e
        tb_str = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        tb_str = "".join(tb_str)
        context.set_code(grpc.StatusCode.UNKNOWN)
        context.set_details(tb_str)
        context.abort(grpc.StatusCode.UNKNOWN, tb_str)
        logger.exception("An Error Occured When calling MessageToDict on 'request' for client request print: \n", exc_info=e)
        context.abort(grpc.StatusCode.UNKNOWN, tb_str)
        
    logger.info("Request Received From {ip}:{port}".format(ip=ip, port=port))
    logger.info('Request Proto:\n' + json.dumps(request, indent=4))
    logger.info(request)
    return ip, port, request