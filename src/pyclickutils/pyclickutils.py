#
# (c) 2025 Yoichi Tanibayashi
#
from . import __package__
from .version import __version__


def import_click(async_flag=False):
    """Import asyncclick or click."""
    # 重要: 下記、コメントの ``# type: ...`` は、mypy対策で必要
    if async_flag:
        import asyncclick as click  # type: ignore[import]
    else:
        import click  # type:ignore[no-redef]

    return click


click = import_click()


def click_common_opts(
    click,
    ver_str: str = "",
    use_h: bool = True, use_d: bool = True, use_v: bool = False
):
    """共通オプションをまとめたメタデコレータ"""
    def _decorator(func):
        decorators = []

        if len(ver_str) > 0:
            v_str = ver_str
        else:
            v_str = f"_._._ ({__package__} {__version__})"

        # version option
        ver_opts = ["--version", "-V"]
        if use_v:
            ver_opts.append("-v")
        decorators.append(
            click.version_option(
                v_str, *ver_opts, message="%(prog)s %(version)s"
            )
        )

        # debug option
        debug_opts = ["--debug"]
        if use_d:
            debug_opts.append("-d")
        decorators.append(
            click.option(*debug_opts, is_flag=True, help="debug flag")
        )

        # help option
        help_opts = ["--help"]
        if use_h:
            help_opts.append("-h")
        decorators.append(click.help_option(*help_opts))

        # decorators をまとめて適用
        for dec in reversed(decorators):
            func = dec(func)

        # context を最後に wrap
        return click.pass_context(func)

    return _decorator
