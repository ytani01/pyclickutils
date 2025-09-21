# tests/test_base.py
#
# `conftest.py` の動作確認用テストプログラム
#
# `cli_runner`: conftest.pyで定義されたフィクスチャー
#
import pytest

class TestBasicCommands:
    @pytest.mark.parametrize(
        "command, expected",
        [
            (["echo", "Hello"], "Hello\n"),
            (["echo", "-n", "No newline"], "No newline"),
        ],
    )
    def test_echo(self, cli_runner, command, expected):
        result = cli_runner.run_command(command)
        cli_runner.assert_output_equals(result, stdout=expected)


class TestAdvancedCommands:
    @pytest.mark.parametrize(
        "input_name, expected",
        [
            ("World", "Hello World"),
            ("Alice", "Hello Alice"),
        ],
    )
    def test_command_with_input(self, cli_runner, input_name, expected):
        result = cli_runner.run_command(
            ["python3", "-c", "name = input(); print('Hello ' + name)"],
            input_data=input_name + "\n",
        )
        cli_runner.assert_output_contains(result, stdout=expected)
