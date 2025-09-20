import pytest
import subprocess


RESULT_OK = 0

SAMPLES_DIR = "samples"

SAMPLE1 = "sample1-simple.py"
SAMPLE2 = "sample2-arg-opt.py"
SAMPLE3 = "sample3-subs.py"
SAMPLE4 = "sample4-async.py"

SAMPLE1_CMD = f"{SAMPLE1}"
SAMPLE2_CMD = f"{SAMPLE2} arg_dummy -o opt_dummy"


def mkcmdline(cmd: str, opt: str = ""):
    """make command line string."""
    cmdline = f"uv run {SAMPLES_DIR}/{cmd}"
    if opt:
        cmdline += f" --{opt}"
    return cmdline


def print_result(result):
    """print result"""
    print(f"* stdout\n'{result.stdout}'")
    print(f"* stderr\n'{result.stderr}'")
    print(f"* returncode = {result.returncode}\n")


@pytest.fixture(autouse=True)
def setup_and_teardown():
    yield


def pattern1(
    cmd: str, opt: str, result_stdout: list[str], result_stderr: list[str]
):
    """test pattern #1"""
    cmdline = mkcmdline(cmd, opt)
    print(f"\n* cmdline = {cmdline}")

    result = subprocess.run(cmdline.split(), capture_output=True, text=True)

    print_result(result)

    assert result.returncode == RESULT_OK
    if result_stdout:
        for s in result_stdout:
            assert s in result.stdout
    if result_stderr:
        for s in result_stderr:
            assert s in result.stdout


class TestSamples:
    """test sample programs"""

    @pytest.mark.parametrize(
        "sample_cmd, option, expected_stdout",
        [
            (SAMPLE1_CMD, "", ["Hello, world!"]),
            (SAMPLE1_CMD, "help", [f"Usage: {SAMPLE1}"]),
            (SAMPLE1_CMD, "version", [f"{SAMPLE1} "]),
            (SAMPLE1_CMD, "debug", ["[DEBUG] "]),
            (SAMPLE2_CMD, "", ["arg1", "arg_dummy", "opt1", "opt_dummy"]),
            (SAMPLE2_CMD, "help", [f"Usage: {SAMPLE2}", "Options:"]),
            (SAMPLE2_CMD, "version", [f"{SAMPLE2} "]),
            (SAMPLE2_CMD, "debug", ["arg1 =", "opt1 =", "[DEBUG] "]),
        ],
    )
    def test_common_options(self, sample_cmd, option, expected_stdout):
        """test common options"""
        pattern1(sample_cmd, option, expected_stdout, [])
