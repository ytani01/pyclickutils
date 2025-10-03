#
# 非同期のサンプル
#
# **重要**
#  - ``click``は、非同期対応してない。
#  - ``asyncclickは``、バグがあり、使い物にならない。
#  - **回避策**: 通常の main から、asyncio.run で async_main を呼び出す。
#
#
#  func1()
#    |    func2()
#    |      |    func3
#    |      |      |
#  2 sec  1 sec  1.5 sec
#    |      |      |
#    |     done    |
#    |            done
#   done
#
import asyncio

import click

from pyclickutils import click_common_opts


async def func1():
    """async func #1."""
    print(" func1 start ..")
    await asyncio.sleep(2)
    print(" func1 done.")


async def func2():
    """async func #2."""
    print("  func2 start ..")
    await asyncio.sleep(1)
    print("  func2 done.")


async def func3():
    """async func #3."""
    print("    func3 start ..")
    await asyncio.sleep(1.5)
    print("    func3 done.")


async def async_main(ctx, debug):
    """async main."""
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
@click_common_opts("4.0.0")
def main(ctx, debug):
    """normal main.

       asyncio.run(async_main())
    """
    print("main> call async_main()")

    result = asyncio.run(async_main(ctx, debug))  # 重要！

    print(f"main> result from async_main(): {result}")



if __name__ == "__main__":
    main()
