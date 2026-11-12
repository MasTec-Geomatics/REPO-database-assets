"""The `repo-load` command."""

import argparse
from collections.abc import Sequence

import structlog

from repo_loaders.config import ConfigError, load_settings
from repo_loaders.layers import LAYERS
from repo_loaders.log import configure_logging

log = structlog.get_logger()


def build_parser() -> argparse.ArgumentParser:
    available = ", ".join(sorted(LAYERS)) or "none yet"
    parser = argparse.ArgumentParser(
        prog="repo-load",
        description="Load a public data layer into the REPO database.",
    )
    parser.add_argument(
        "layer",
        metavar="LAYER",
        choices=sorted(LAYERS),
        help=f"layer to load (available: {available})",
    )
    parser.add_argument("-v", "--verbose", action="store_true", help="show debug logging")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    configure_logging(verbose=args.verbose)
    layer_log = log.bind(layer=args.layer)

    try:
        settings = load_settings()
        LAYERS[args.layer](settings)
    except ConfigError as exc:
        layer_log.error("configuration error", error=str(exc))
        return 2
    except Exception:
        layer_log.exception("load failed")
        return 1

    layer_log.info("load finished")
    return 0
