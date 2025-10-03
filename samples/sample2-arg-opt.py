#
#  独自の引数やオプションを加えるサンプル
#
# `click.command()` と `@click_common_opts()` ではさむ
#
import click

from pyclickutils import click_common_opts


@click.command()
@click.argument("arg1", nargs=-1)
@click.option("--opt1", "-o", type=str)
@click_common_opts("0.0.2")
def main(ctx, arg1, opt1, debug):
    if debug:
        print(f"[DEBUG] click = '{click.__name__}'")
        print(f"[DEBUG] command.name = '{ctx.command.name}'")

    print(f"arg1 = '{arg1}'")
    print(f"opt1 = '{opt1}'")


if __name__ == "__main__":
    main()
