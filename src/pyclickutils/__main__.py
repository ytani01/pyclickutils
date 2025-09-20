#
# (c) 2025 Yoichi Tanibayashi
#
import click
from . import __version__, click_common_opts, get_logger


@click.group(invoke_without_command=True)
@click_common_opts(click, __version__)
def cli(ctx, debug):
    """CLI top."""

    __log = get_logger(__name__, debug)
    __log.debug("click = %a", click.__name__)
    __log.debug("command name = %a", ctx.command.name)
    # __log.debug("ctx = %s", pprint.pformat(vars(ctx)))
    # __log.debug("ctx = %s", pprint.pformat(vars(ctx)))

    print(f"{ctx.command.name}")

    if ctx.invoked_subcommand:
        __log.debug("subcommand = %a", ctx.invoked_subcommand)
    else:
        print(ctx.get_help())


@cli.command()
@click_common_opts(click, __version__)
def sub1(ctx, debug):
    """Subcommand #1."""
    __log = get_logger(__name__, debug)
    __log.debug("command name = %a", ctx.command.name)

    print(f"  {ctx.command.name}")


@cli.group(invoke_without_command=True)
@click_common_opts(click, __version__)
def sub2(ctx, debug):
    """Subcommand #2.(command group)"""

    __log = get_logger(__name__, debug)
    __log.debug("command name = %a", ctx.command.name)
    # __log.debug("ctx = %s", pprint.pformat(vars(ctx)))
    # __log.debug("ctx = %s", pprint.pformat(vars(ctx)))

    print(f"  {ctx.command.name}")

    if ctx.invoked_subcommand:
        __log.debug("subcommand = %a", ctx.invoked_subcommand)
    else:
        print(ctx.get_help())


@sub2.command()
@click_common_opts(click, __version__)
def sub2sub(ctx, debug):
    """Subcommand of `sub2`."""
    __log = get_logger(__name__, debug)
    __log.debug("command name = %a", ctx.command.name)

    print(f"    {ctx.command.name}")
