"""structlog setup: readable console output in a terminal, JSON everywhere else."""

import importlib.util
import logging
import sys

import structlog
from structlog.typing import ExceptionRenderer, Processor


def configure_logging(*, verbose: bool = False) -> None:
    shared: list[Processor] = [
        structlog.contextvars.merge_contextvars,
        structlog.processors.add_log_level,
        structlog.processors.TimeStamper(fmt="iso", utc=True),
        structlog.processors.StackInfoRenderer(),
    ]

    # show_locals=False keeps local variables (which can hold credentials) out of tracebacks.
    renderers: list[Processor]
    if sys.stderr.isatty():
        # rich is a dev-only dependency; fall back to plain tracebacks where it isn't installed.
        exception_formatter: ExceptionRenderer = (
            structlog.dev.RichTracebackFormatter(show_locals=False)
            if importlib.util.find_spec("rich") is not None
            else structlog.dev.plain_traceback
        )
        renderers = [structlog.dev.ConsoleRenderer(exception_formatter=exception_formatter)]
    else:
        renderers = [
            structlog.processors.ExceptionRenderer(
                structlog.tracebacks.ExceptionDictTransformer(show_locals=False)
            ),
            structlog.processors.JSONRenderer(),
        ]

    structlog.configure(
        processors=shared + renderers,
        wrapper_class=structlog.make_filtering_bound_logger(
            logging.DEBUG if verbose else logging.INFO
        ),
        logger_factory=structlog.PrintLoggerFactory(file=sys.stderr),
        cache_logger_on_first_use=True,
    )
