# tests/conftest.py
import pytest
import subprocess
import pty
import os
import select
import time
from typing import Optional


class InteractiveSession:
    def __init__(self, master_fd, process):
        self.master_fd = master_fd
        self.process = process
        self.output = ""

    def send_key(self, key: str):
        """Sends a key press to the process."""
        os.write(self.master_fd, key.encode())

    def expect(self, pattern: str, timeout: int = 5) -> bool:
        """Waits for a pattern to appear in the output."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            r, _, _ = select.select([self.master_fd], [], [], 0.1)
            if r:
                try:
                    data = os.read(self.master_fd, 1024).decode()
                    self.output += data
                    print(f"Current output: {self.output!r}") # Debug print
                    if pattern in self.output:
                        return True
                except OSError:
                    break
        return False

    def get_output(self) -> str:
        """Returns the captured output."""
        return self.output

    def close(self):
        """Terminates the process and closes the file descriptor."""
        self.process.terminate()
        self.process.wait()
        os.close(self.master_fd)


class CLITestBase:
    """CLIテスト用のヘルパークラス。

    コマンドの実行、出力のアサーションなど、CLIテストで頻繁に使用する機能を提供します。
    """
    DEFAULT_TIMEOUT = 10
    DEFAULT_ENCODING = "utf-8"

    def run_command(
        self,
        command: list[str],
        input_data: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        cwd: Optional[str] = None,
        env: Optional[dict[str, str]] = None,
        check_success: bool = True,
    ) -> subprocess.CompletedProcess:
        """コマンドを実行し、結果を返します。

        Args:
            command: 実行するコマンドのリスト。
            input_data: 標準入力に渡すデータ。
            timeout: コマンドのタイムアウト（秒）。
            cwd: コマンドを実行するディレクトリ。
            env: コマンドの環境変数。
            check_success: Trueの場合、コマンドが失敗したらpytest.failを呼び出します。

        Returns:
            コマンドの実行結果。

        Raises:
            pytest.fail: コマンドの実行に失敗した場合。
            pytest.skip: コマンドが見つからない場合。
        """
        try:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding=self.DEFAULT_ENCODING,
                input=input_data,
                timeout=timeout,
                cwd=cwd,
                env=env,
            )
            if check_success and result.returncode != 0:
                pytest.fail(
                    f"Command failed: {' '.join(command)}\n"
                    f"Return code: {result.returncode}\n"
                    f"Stdout: {result.stdout}\n"
                    f"Stderr: {result.stderr}"
                )
            return result
        except subprocess.TimeoutExpired:
            command_str = " ".join(command)
            # noqa: E501
            pytest.fail(f"Command timed out after {timeout}s: {command_str}")
        except FileNotFoundError:
            pytest.skip(f"Command not found: {command[0]}")

    def run_interactive_command(self, command: list[str]) -> "InteractiveSession":
        master_fd, slave_fd = pty.openpty()
        process = subprocess.Popen(
            command,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            close_fds=True,
        )
        os.close(slave_fd)
        return InteractiveSession(master_fd, process)

    def assert_output_contains(
        self,
        result: subprocess.CompletedProcess,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> None:
        """標準出力または標準エラー出力に特定の文字列が含まれていることを表明します。"""
        if stdout is not None:
            assert stdout in result.stdout, (
                f"Expected '{stdout}' in stdout, got: {result.stdout!r}"
            )
        if stderr is not None:
            assert stderr in result.stderr, (
                f"Expected '{stderr}' in stderr, got: {result.stderr!r}"
            )

    def assert_output_equals(
        self,
        result: subprocess.CompletedProcess,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> None:
        """stdout, stderrが特定の内容と完全に一致することを確認"""
        if stdout is not None:
            assert result.stdout == stdout, (
                f"Expected stdout: {stdout!r}, got: {result.stdout!r}"
            )
        if stderr is not None:
            assert result.stderr == stderr, (
                f"Expected stderr: {stderr!r}, got: {result.stderr!r}"
            )

    def assert_return_code(
        self, result: subprocess.CompletedProcess, expected: int
    ) -> None:
        """コマンドの終了コードが期待値と一致することを表明します。"""
        assert result.returncode == expected, (
            f"Expected return code {expected}, got {result.returncode}\n"
            f"Stdout: {result.stdout}\n"
            f"Stderr: {result.stderr}"
        )


@pytest.fixture
def cli_runner():
    """CLI テスト基盤を fixture として提供（インスタンスを返す）"""
    return CLITestBase()


# Key Constants for Interactive Testing
KEY_UP = "\x1b[A"
KEY_DOWN = "\x1b[B"
KEY_RIGHT = "\x1b[C"
KEY_LEFT = "\x1b[D"
KEY_ENTER = "\n"
