#
# (c) 2025 Yoichi Tanibayashi
#
from importlib.metadata import version as get_version

from .mylogger import errmsg, get_logger
from .pyclickutils import click_common_opts

if __package__:
    __version__ = get_version(__package__)
else:
    __version__ = "?.?.?"


__all__ = [
    "__version__",
    "click_common_opts",
    "errmsg",
    "get_logger",
]
