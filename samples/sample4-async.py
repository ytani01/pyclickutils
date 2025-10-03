#
# 非同期のサンプル
#
# **重要**
#  - ``click``は、非同期対応してない。
#  - ``asyncclickは``、バグがあり、使い物にならない。
#  - 回避策: 通常の main から、asyncio.run で、async_main を呼び出す。
#
import asyncio

import click

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


async def async_main(ctx, debug):
    """非同期関数用main."""
    if debug:
        print(f"[DEBUG] async_main> command.name = '{ctx.command.name}'")
        print("[DEBUG] async_main> call async functions ..")
    await asyncio.gather(
        func1(),
        func2(),
        func3()
    )
    if debug:
        print("[DEBUG] async_main> all done.")
    return "done"


@click.command()
@click_common_opts(click, "0.0.1")
def main(ctx, debug):
    """main.
    asyncio.run(async_main())
    """
    if debug:
        print(f"[DEBUG] main> command.name = '{ctx.command.name}'")

    print(f"{ctx.command.name}> call async_main()")
    result = asyncio.run(async_main(ctx, debug))  # 重要！
    print(result)


if __name__ == "__main__":
    main()
