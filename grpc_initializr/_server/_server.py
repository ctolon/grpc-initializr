from concurrent import futures
from enum import Enum
from typing import List, Union
import argparse
import asyncio
import logging

import grpc

from .._consts import _Constants as settings


class _GRPCServerTypes(str, Enum):
    """GRPC Server Types."""
    
    SYNC = 'SYNC'
    ASYNC = 'ASYNC'


class GRPCServer(object):
    """GRPC Server Object."""

    @property
    def instance(self):
        return self.__server
    
    @property
    def logger(self):
        return self.__logger

    def __init__(
        self,
        address=settings.GRPC_HOST,
        port=settings.GRPC_HOST,
        max_workers=10,
        options=settings.GRPC_SERVER_OPTS,
        server_type=_GRPCServerTypes.ASYNC,
        logger: logging.Logger = None,
        sync_servicers: List[object] = None,
        async_servicers: List[object] = None
        ):
        self.__address = address
        self.__port = port
        
        # Initialize GRPC Server as Singleton
        self.__logger = logger
        
        # Intialize Servicers
        self.__async_servicers = async_servicers
        self.__sync_servicers = sync_servicers
        
        if not(sync_servicers or async_servicers):
            raise Exception("Servicers is None! You should define at least one servicer.")
        
        # Initialize GRPC Server as Async or Sync
        self.__enums = [e.value for e in _GRPCServerTypes]
        self.__logger.info("GRPC Server Type: {server_type}".format(server_type=server_type))
        if server_type not in self.__enums:
            raise TypeError("Invalid GRPC Server Type! Please choose from {enums}".format(enums=self.__enums))
        
        if server_type == _GRPCServerTypes.SYNC:
            self.__server = grpc.server(futures.ThreadPoolExecutor(max_workers=max_workers), options=options)
        else:
            self.__server = grpc.aio.server(options=options)


    def serve(self):
        endpoint = '{address}:{port}'.format(
            address=self.__address,
            port=str(self.__port)
        )
        
        if self.__async_servicers is None:
            raise Exception("Async Servicers is None!")
        self._add_servicer_to_server(self.__async_servicers)

        self.logger.info(f'Started GRPC Server at {endpoint}')
        self.logger.info('Serving...')

        self.__server.add_insecure_port(endpoint)
        self.__server.start()
        self.__server.wait_for_termination()
        
    async def aio_serve(self):
        endpoint = '{address}:{port}'.format(
            address=self.__address,
            port=str(self.__port)
        )
        
        if self.__sync_servicers is None:
            raise Exception("Sync Servicers is None!")
        self._add_servicer_to_server(self.__async_servicers)

        self.logger.info(f'Started GRPC Server at {endpoint}')
        self.logger.info('Serving...')

        self.__server.add_insecure_port(endpoint)
        await self.__server.start()
        await self.__server.wait_for_termination()

    def stop(self):
        self.logger.info("Stopping GRPC Server gracefully")
        self.__server.stop(3)
        
    def _add_servicer_to_server(self, servicer_list: List[object]):
        """Servicer List is a list of servicer object.
        
        Example:
        
        servicer_list = [
            groom_pb2_grpc.add_GroomServicer_to_server(GroomService(), server.instance)
            ]
        """
        
        for servicer in servicer_list:
            servicer
    
def run_grpc_cli(
    logger: Union[logging.Logger, None] = None,
    sync_servicers: List[object] = None,
    async_servicers: List[object] = None
):
    """Run GRPC Server CLI.

    Args:
        logger (logging.Logger, optional): Logger Object. Defaults to None.
        sync_servicers (List[object], optional): List of Servicers for sync gRPC. Defaults to None.
        async_servicers (List[object], optional): List of Servicers for async gRPC. Defaults to None.

    Raises:
        Exception: If no servicer defined for gRPC.
        Exception: If no async servicer defined for async gRPC or no sync servicer defined for sync gRPC.
    """
    
    if not(sync_servicers or async_servicers):
        raise Exception("Servicers is None! You should define at least one servicer.")
    
    parser = argparse.ArgumentParser(description="GRPC Server CLI")
    parser.add_argument("--host", "-H", help="GRPC Server Host", type=str, required=False, default=settings.GRPC_HOST)
    parser.add_argument("--port", "-p", help="GRPC Server Port", type=str, required=False, default=settings.GRPC_PORT)
    parser.add_argument("--worker", "-w", help="Num of Workers as Thread in Threadpool for concurrency", type=int, required=False, default=settings.WORKER)
    parser.add_argument("--server-type", "-st", help="GRPC Server Type", type=str.upper, required=False, default=_GRPCServerTypes.SYNC.value, choices=list(_GRPCServerTypes))
    args = parser.parse_args()
        
    port = args.port
    worker = args.worker
    host = args.host
    server_type = args.server_type
    
    server = GRPCServer(address=host, port=port, max_workers=worker, server_type=server_type, logger=logger, sync_servicers=sync_servicers, async_servicers=async_servicers)
    
    # For sync gRPC, Workers shouldn't be less than 10
    if worker < 10:
        worker = 10
    
    # Start gRPC Server as SYNC
    if server_type == _GRPCServerTypes.SYNC:
        if sync_servicers is None:
            raise Exception("Sync Servicers is None!")
        server.serve()
        
    # Start gRPC Server as ASYNC
    elif server_type == _GRPCServerTypes.ASYNC:
        if async_servicers is None:
            raise Exception("Async Servicers is None!")
        logger.info("Workers is not used for Async GRPC Server! (gRPC aio uses asyncio instead of threadpool)")
        asyncio.run(server.aio_serve())