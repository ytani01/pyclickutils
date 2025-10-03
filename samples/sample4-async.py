#
# 非同期のサンプル
#
import asyncio

import asyncclick as click

from pyclickutils import click_common_opts


async def func1():
    """非同期関数 #1."""
    print(" func1 start ..")
    await asyncio.sleep(2)
    print(" func1 done.")


async def func2():
    """非同期関数 #2."""
    print("  func2 start ..")
    await asyncio.sleep(1)
    print("  func2 done.")


async def func3():
    """非同期関数 #3."""
    print("    func3 start ..")
    await asyncio.sleep(1.5)
    print("    func3 done.")


@click.group()
@click_common_opts(click, "0.0.1")
async def main(ctx, debug):
    pass


@main.command()
@click_common_opts(click, "0.0.1")
async def sub(ctx, debug):
    """非同期main."""
    if debug:
        print(f"[DEBUG] click        = '{click.__name__}'")
        print(f"[DEBUG] command.name = '{ctx.command.name}'")

    print("call async functions ..")
    await asyncio.gather(
        func1(),
        func2(),
        func3()
    )
    print("all done.")


if __name__ == "__main__":
    main()  # 普通に呼び出す。(async.. とか、awaitとか、不要)
