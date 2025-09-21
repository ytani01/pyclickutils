# tests/conftest.py
import pytest
import subprocess
from typing import List, Optional, Dict


class CLITestBase:
    """CLI テスト用の基底クラス"""
    DEFAULT_TIMEOUT = 10
    DEFAULT_ENCODING = "utf-8"

    def run_command(
        self,
        command: List[str],
        input_data: Optional[str] = None,
        timeout: int = DEFAULT_TIMEOUT,
        cwd: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        check_success: bool = True,
    ) -> subprocess.CompletedProcess:
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
            pytest.fail(f"Command timed out after {timeout}s: {' '.join(command)}")
        except FileNotFoundError:
            pytest.skip(f"Command not found: {command[0]}")

    def assert_output_contains(
        self,
        result: subprocess.CompletedProcess,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> None:
        if stdout is not None:
            assert stdout in result.stdout, f"Expected '{stdout}' in stdout, got: {result.stdout!r}"
        if stderr is not None:
            assert stderr in result.stderr, f"Expected '{stderr}' in stderr, got: {result.stderr!r}"

    def assert_output_equals(
        self,
        result: subprocess.CompletedProcess,
        stdout: Optional[str] = None,
        stderr: Optional[str] = None,
    ) -> None:
        if stdout is not None:
            assert result.stdout == stdout, f"Expected stdout: {stdout!r}, got: {result.stdout!r}"
        if stderr is not None:
            assert result.stderr == stderr, f"Expected stderr: {stderr!r}, got: {result.stderr!r}"

    def assert_return_code(self, result: subprocess.CompletedProcess, expected: int) -> None:
        assert result.returncode == expected, (
            f"Expected return code {expected}, got {result.returncode}\n"
            f"Stdout: {result.stdout}\nStderr: {result.stderr}"
        )


@pytest.fixture
def cli_runner():
    """CLI テスト基盤を fixture として提供（インスタンスを返す）"""
    return CLITestBase()
