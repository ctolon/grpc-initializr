import logging
from pathlib import Path

from .._consts import _Constants

class _SingletonType(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(_SingletonType, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class _GRPCLogger(object, metaclass=_SingletonType):
    
    _logger = None
    
    def __init__(
        self,
        logger_name=_Constants.LOGGER_NAME,
        add_file_handler=False,
        add_stream_handler=True,
        log_level=_Constants.LOG_LEVEL,
        log_fmt=_Constants.LOG_FORMAT,
        log_datefmt=_Constants.LOG_DATEFMT,
        log_path=None
        ):
    
        self._logger = logging.getLogger(logger_name)
        self._logger.setLevel(log_level)
        formatter = logging.Formatter(log_fmt, log_datefmt)
        
        # Add File Handler
        if add_file_handler and log_path is not None:
            if not Path(log_path).exists():
                Path(log_path).mkdir(exist_ok=True)
            log_file_path = str(log_path / logger_name + ".log")
            fileHandler = logging.FileHandler(filename=log_file_path, mode="a", encoding="utf-8")
            fileHandler.setFormatter(formatter)
            self._logger.addHandler(fileHandler)
        
        # Add Stream Handler
        if add_stream_handler:
            streamHandler = logging.StreamHandler()
            streamHandler.setFormatter(formatter)
            self._logger.addHandler(streamHandler)
        
        self._logger.info("{} Logger initialized as singleton.".format(logger_name))
        
    @property
    def get_logger(self) -> logging.Logger:
        logger = self._logger
        if logger is None:
            raise Exception("Logger not initialized yet.")
        
        return logger