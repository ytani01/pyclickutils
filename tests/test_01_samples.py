import subprocess

import pytest

SAMPLES_DIR = "samples"

SAMPLE = [
    "__dummy__",
    "sample1-simple.py",
    "sample2-arg-opt.py",
    "sample3-subs.py",
    "sample4-async.py",
]
SAMPLE_CMD = [
    "__dummy__",
    f"{SAMPLE[1]}",
    f"{SAMPLE[2]} arg1 arg2 -o opt1",
    [
        f"{SAMPLE[3]}",
        f"{SAMPLE[3]} sub",
        f"{SAMPLE[3]} sub subsub",
    ],
    f"{SAMPLE[4]}",
]


@pytest.fixture(autouse=True)
def setup_and_teardown():
    yield


class TestSamples:
    """test sample programs"""
    @pytest.mark.parametrize(
        "cmd, opt, expected_stdout, expected_stderr, returncode",
        [
            (
                SAMPLE_CMD[1], "",
                ["Hello, world!"],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "--help",
                [f"Usage: {SAMPLE[1]}", "Options"],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "-h",
                [f"Usage: {SAMPLE[1]}", "Options"],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "--version",
                [
                    f"{SAMPLE[1]} "
                ],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "-V",
                [f"{SAMPLE[1]} "],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "--debug",
                ["[DEBUG] ", "command.name", "main"],
                [],
                0
            ),
            (
                SAMPLE_CMD[1], "-d",
                ["[DEBUG] ", "command.name", "main"],
                [],
                0
            ),
            (
                SAMPLE_CMD[2], "",
                ["arg1", "arg2", "opt1"],
                [],
                0
            ),
            (
                SAMPLE_CMD[2], "--help",
                [f"Usage: {SAMPLE[2]}", "Options:"],
                [],
                0
            ),
            (
                SAMPLE_CMD[2], "--version",
                [f"{SAMPLE[2]} "],
                [],
                0
            ),
            (
                SAMPLE_CMD[2], "--debug",
                ["arg1 =", "opt1 =", "[DEBUG] "],
                [],
                0
            ),
            (
                SAMPLE_CMD[3][0], "",
                [],
                [
                    f"Usage: {SAMPLE[3]}",
                    "Options:",
                    "Commands:",
                    "sub"
                ],
                2
            ),
            (
                SAMPLE_CMD[3][0], "-V",
                [f"{SAMPLE[3]} "],
                [],
                0
            ),
            (
                SAMPLE_CMD[3][0], "-d",
                [],
                [f"Usage: {SAMPLE[3]} ", "Error: Missing command."],
                2
            ),
            (
                SAMPLE_CMD[3][1], "",
                [],
                [
                    f"Usage: {SAMPLE[3]}",
                    "Options:",
                    "Commands:",
                    "sub"
                ],
                2
            ),
            (
                SAMPLE_CMD[3][1], "-V",
                [f"{SAMPLE[3]} "],
                [],
                0
            ),
            (
                SAMPLE_CMD[3][2], "",
                ["Hello, world"],
                [],
                0
            ),
            (
                SAMPLE_CMD[4], "",
                [
                    "call async",
                    "func1 start",
                    "func2 start",
                    "func3 start",
                    "func1 done",
                    "func2 done",
                    "func3 done",
                    "done"
                ],
                [],
                0
            ),
            (
                SAMPLE_CMD[4], "-h",
                ["Usage: ", "Options:"],
                [],
                0
            ),
            (
                SAMPLE_CMD[4], "-d",
                ["[DEBUG] ", "done",],
                [],
                0
            ),
        ],
    )
    def test_common_options(
            self, cli_runner, cmd, opt, expected_stdout, expected_stderr, returncode
    ):
        """test common options"""
        cmdline = f"uv run {SAMPLES_DIR}/{cmd}"
        cli_runner.test_command(
            cmdline, opt,
            e_stdout=expected_stdout,
            e_stderr=expected_stderr,
            e_ret=returncode
        )
