#
# シンプルなサンプル
#
#   これだけで、以下のオプションが使えるようになります。
#
"""
Options:
  -V, --version  Show the version and exit.
  -d, --debug    debug flag
  -h, --help     Show this message and exit.
"""
import click

from pyclickutils import click_common_opts


@click.command()
@click_common_opts(click, "0.0.1")
def main(ctx, debug):
    if debug:
        print(f"[DEBUG] command.name = '{ctx.command.name}'")

    print("Hello, world!")


if __name__ == "__main__":
    main()
