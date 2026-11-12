"""Registry of layer loaders, keyed by the name used on the command line."""

from collections.abc import Callable

from repo_loaders.config import Settings

type LayerLoader = Callable[[Settings], None]

LAYERS: dict[str, LayerLoader] = {}
