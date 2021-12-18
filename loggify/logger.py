from __future__ import annotations

import logging
import os
import sys
import traceback
from types import TracebackType
from typing import Optional, TextIO, Type

_STDOUT_LOGGER_NAME = "STDOUT"
_STDERR_LOGGER_NAME = "STDERR"


class Loggify:
    """Loggify context manager."""

    def __init__(
        self,
        filename: str,
        filemode: str = "a",
        replace: bool = False,
        linefmt: str = "%(asctime)s.%(msecs)03d:%(name)s:%(message)s",
        datefmt: str = "%Y-%m-%d %H:%M:%S",
    ) -> None:
        if replace and os.path.isfile(filename):
            os.remove(filename)
        self.stdout_logger = self._get_stdout_logger(
            filename=filename,
            filemode=filemode,
            linefmt=linefmt,
            datefmt=datefmt,
        )
        self.stderr_logger = self._get_stderr_logger(
            filename=filename,
            filemode=filemode,
            linefmt=linefmt,
            datefmt=datefmt,
        )

    def _get_stdout_logger(
        self,
        filename: str,
        filemode: str,
        linefmt: str,
        datefmt: str,
    ) -> StreamToLogger:
        level = logging.INFO
        logger = logging.getLogger(name=_STDOUT_LOGGER_NAME)
        logger.setLevel(level=level)
        formatter = logging.Formatter(fmt=linefmt, datefmt=datefmt)
        file_handler = logging.FileHandler(filename=filename, mode=filemode)
        file_handler.setLevel(level=level)
        file_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=file_handler)
        stdout_logger = StreamToLogger(
            stream=sys.__stdout__,
            logger=logger,
            level=level,
            encoding="utf-8",
        )
        return stdout_logger

    def _get_stderr_logger(
        self,
        filename: str,
        filemode: str,
        linefmt: str,
        datefmt: str,
    ) -> StreamToLogger:
        level = logging.ERROR
        logger = logging.getLogger(name=_STDERR_LOGGER_NAME)
        logger.setLevel(level=level)
        formatter = logging.Formatter(fmt=linefmt, datefmt=datefmt)
        file_handler = logging.FileHandler(filename=filename, mode=filemode)
        file_handler.setLevel(level=level)
        file_handler.setFormatter(fmt=formatter)
        logger.addHandler(hdlr=file_handler)
        stderr_logger = StreamToLogger(
            stream=sys.__stderr__,
            logger=logger,
            level=level,
            encoding="utf-8",
        )
        return stderr_logger

    def __enter__(self) -> "Loggify":
        sys.stdout = self.stdout_logger
        sys.stderr = self.stderr_logger
        return self

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        exc_traceback: Optional[TracebackType],
    ) -> bool:
        if exc_type or exc_value or exc_traceback:
            exc = "".join(
                traceback.format_exception(exc_type, exc_value, exc_traceback)
            )
            self.stderr_logger.write(exc, to_stream=False)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        return False


class StreamToLogger:
    """Stream object that redirects writes to a logger instance."""

    def __init__(
        self,
        stream: TextIO,
        logger: logging.Logger,
        level: int,
        encoding: str,
    ) -> None:
        self.stream = stream
        self.logger = logger
        self.level = level
        self.encoding = encoding
        self._linebuf = ""

    def write(self, data: str, to_stream: bool = True) -> None:
        if isinstance(data, bytes):
            self.stream.write(data.decode("utf-8"))
            return
        if to_stream:
            self.stream.write(data)
        linebuf = self._linebuf + data
        self._linebuf = ""
        for line in linebuf.splitlines(True):
            if line[-1] == "\n":
                self.logger.log(self.level, line.rstrip("\n"))
            else:
                self._linebuf += line

    def isatty(self) -> bool:
        return hasattr(self.stream, "isatty") and self.stream.isatty()

    def flush(self) -> None:
        self.stream.flush()
        if self._linebuf != "":
            self.logger.log(self.level, self._linebuf.rstrip("\n"))
        self._linebuf = ""

    def fileno(self) -> int:
        return self.stream.fileno()
