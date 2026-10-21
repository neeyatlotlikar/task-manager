import logging
import queue
from logging.handlers import QueueHandler, QueueListener, RotatingFileHandler
from pathlib import Path


class NonBlockingQueueHandler(QueueHandler):
    def __init__(
        self,
        filename: str | Path,
        formatter: logging.Formatter | None = None,
        level: int = logging.NOTSET,
        max_bytes: int = 5 * 1024 * 1024,
        backup_count: int = 5,
    ):
        log_queue = queue.SimpleQueue()
        super().__init__(log_queue)
        self.setLevel(level)

        log_path = Path(filename)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        console_handler = logging.StreamHandler()
        file_handler = RotatingFileHandler(
            log_path,
            maxBytes=max_bytes,
            backupCount=backup_count,
            encoding="utf-8",
            delay=True,
        )
        if formatter is not None:
            console_handler.setFormatter(formatter)
            file_handler.setFormatter(formatter)

        self.listener = QueueListener(
            self.queue,
            console_handler,
            file_handler,
            respect_handler_level=True,
        )
        self.listener.start()

    def close(self):
        self.listener.stop()
        super().close()
