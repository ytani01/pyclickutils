#
# (c) 2025 Yoichi Tanibayashi
#
from importlib.metadata import version as get_version

from .my_logger import get_logger
from .pyclickutils import click_common_opts

if __package__:
    __version__ = get_version(__package__)
else:
    __version__ = "0.0.0.none"


__all__ = [
    "__package__",
    "__version__",
    "click_common_opts",
    "get_logger",
]
