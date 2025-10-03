import asyncio

import click


# 外部の async メソッド
async def fetch_data():
    await asyncio.sleep(1)
    return "データ取得完了"

@click.command()
def main():
    """CLIから外部 async を呼ぶ例"""
    # 自分でイベントループを回す
    result = asyncio.run(fetch_data())
    print(result)

if __name__ == "__main__":
    main()
