#
# サブコマンドを定義するサンプル。
#
# サブコマンドごとに、個別にバージョン設定可能
# コマンドグループ・サブコマンドごとにデバッグオプション
#
# e.g.   ``... sample3-sub -d sub -d subsub -d``
#
import click

from pyclickutils import click_common_opts


@click.group()
@click_common_opts("1.1.1")
def main(ctx, debug):
    if debug:
        print(f"[DEBUG] command.name = '{ctx.command.name}'")


@main.group()
@click_common_opts("2.2.2")
def sub(ctx, debug):
    if debug:
        print(f"[DEBUG] command.name =   '{ctx.command.name}'")


@sub.command()
@click_common_opts("3.3.3")
def subsub(ctx, debug):
    if debug:
        print(f"[DEBUG] command.name =     '{ctx.command.name}'")

    print("Hello, world")


# ファイルを分ける場合は、以下のように登録する必要があります。
# ※このサンプルでは、同じファイルなので、なくても大丈夫です。
#
# main.add_command(sub)
# sub.add_command(subsub)


if __name__ == "__main__":
    main()
