import logging

import structlog


def configure_logger():
    # Set up root logger to output logs to the console
    if not logging.getLogger().hasHandlers():
        logging.basicConfig(
            level=logging.INFO,  # Set the log level to INFO
            format="%(message)s",  # Simple output format for logs
        )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(logging.INFO),
        context_class=dict,  # The type of context used for the logger
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True
    )
    return structlog.get_logger()
