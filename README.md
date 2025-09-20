# pyclickutils

`pyclickutils` は、Python の `click` ライブラリを使用したコマンドラインインターフェース (CLI) アプリケーション開発を支援するユーティリティ集です。


## == 目的

`click` を用いて CLI アプリケーションを開発する際、バージョン表示、デバッグフラグ、ヘルプ表示といった共通オプションの設定は反復的な作業となりがちです。`pyclickutils` は、これらの共通オプションを単一のデコレータで一括して適用可能にすることで、開発の効率化とコードの一貫性向上に貢献します。


## == 特徴

- **共通オプションの簡素化**

  バージョン、デバッグ、ヘルプといった共通の CLI オプションを、
  `@click_common_opts(...)` デコレータ一つで設定できます。

``` text
    -V, --version  Show the version and exit.
    -d, --debug    debug flag
    -h, --help     Show this message and exit.
```

- **柔軟な設定**

  各オプションのショートカット (`-v`, `-d`, `-h`) の有効/無効を制御可能です。

- **`click` との統合**

  `click` のデコレータとして機能するため、
  既存の `click` アプリケーションに容易に組み込むことができます。


## == 参考情報

- [click: Python package for creating beautiful command line interfaces](https://github.com/pallets/click)


## == インストール

以下は、`uv`で管理された既存のプロジェクト(`myproject`)に、
本パッケージを組み込む方法です。

```bash
cd work   # `myproject`の親ディレクトリに移動

git clone https://github.com/ytani01/pyclickutils.git

# 組み込みたいプロジェクト(`myproject`)の隣に、
# work/pyclickutils/ ディレクトリが作成され、
# 以下のようなディレクトリ構成になります。
# 
# work/
# ├── pyclickutils/
# └── myproject/

cd myproject  # 組み込みたいプロジェクトのディレクトリに移動

uv add ../pyclickutils  # 相対パスで本パッケージを`uv add`する。
```


## == 使用方法

### === `@click_common_opts` デコレータ

`click_common_opts` は、
`click` コマンドやグループに共通オプションを追加するためのデコレータです。
基本的な使用方法は以下の通りです。

その他のサンプルは、[samples](samples/) ディレクトリを参照してください。

※ **注意**
※ 同期/非同期に合わせて以下のインポートを適切に選んでください。
※   import click
※     or
※   import asyncclick as click

```python
import click

from pyclickutils import click_common_opts


VERSION = "1.0.0"


# CLI のトップレベルコマンドを定義
@click.group(invoke_without_command=True)
@click_common_opts(click, VERSION)
def cli(ctx, debug):
    """CLI top."""
    if debug:
        print(f"[DEBUG] command name = '{ctx.command.name}'")
        print(f"[DEBUG] sub command name = '{ctx.invoked_subcommand}'")

    print(f"Hello from {ctx.command.name}")

    if ctx.invoked_subcommand:
        log.debug("subcommand = %a", ctx.invoked_subcommand)
    else:
        print(ctx.get_help())


# サブコマンドを定義
@cli.command()
@click.argument("arg1", type=str, nargs=1)
@click.options("--opt1", type=str, default="")
@click_common_opts(click, VERSION)
def sub1(ctx, arg1, opt1, debug):
    """Subcommand #1."""
    if debug:
        print(f"command name = '{ctx.command.name}'")

    print(f"Hello, {arg1} {opt1}")

if __name__ == '__main__':
    cli()
```


#### ==== パラメータ

- `click` (必須)

   インポートした`click`パッケージを明示的に指定する必要があります。

- `ver_str` (str, 省略可)

  バージョンオプション (`--version`, `-V`) で表示される文字列を指定します。
  省略した場合、プログラム名と、
  **本パッケージの**バージョン情報が設定されます。

- `use_h` (bool, 省略可): デフォルト = `True`

  ヘルプオプションとして、 `-h` を有効にするかどうか。
  `--help` は、常に有効。

- `use_d` (bool, 省略可): デフォルト = `True`

  デバッグオプションとして、`-d` を有効にするかどうか。
  `--debug` は、常に有効。

- `use_v` (bool, 省略可): デフォルト = `False`

  バージョンオプションとして、小文字の `-v` を有効にするかどうか。
  `--version` と `-V` は、常に有効。


### === コマンドラインでの実行例

以下のコマンドで、本パッケージの動作を確認できます。

```bash
# ヘルプの表示
pyclickutils --help
pyclickutils -h

# バージョンの表示
pyclickutils --version
pyclickutils -V
pyclickutils -v # `use_v=True` に設定した場合に有効

# デバッグモードでのサブコマンド実行
pyclickutils --debug sub1
pyclickutils -d sub1

# サブコマンドの実行
pyclickutils sub1
pyclickutils sub2 sub2sub
```


## == ライセンス

このプロジェクトは [MIT License](LICENCE) の下で公開されています。
