import os
import pytest
import subprocess


TEST_ARCHIVE_DIR = "test_archives"
TEST_FILE_NAME = "test_file"
TEST_FILE_EXT = "md"
TEST_FILE = f"{TEST_FILE_NAME}.{TEST_FILE_EXT}"
TEST_FILE_NOTFOUND = "test_file_notfile.md"
TEST_DIR_NOTFOUND = "test_archive_err"

TEST_STAT = "stat1"

RESULT_OK = 0
RESULT_FILE_NOTFOUND = 1
RESULT_DIR_NOTFOUND = 2

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # テスト前にアーカイブディレクトリをクリーンアップ
    # なければ作成する
    if os.path.exists(TEST_ARCHIVE_DIR):
        for f in os.listdir(TEST_ARCHIVE_DIR):
            os.remove(os.path.join(TEST_ARCHIVE_DIR, f))
    else:
        os.makedirs(TEST_ARCHIVE_DIR)

    yield

    # テスト後にアーカイブディレクトリをクリーンアップ
    if os.path.exists(TEST_ARCHIVE_DIR):
        for f in os.listdir(TEST_ARCHIVE_DIR):
            os.remove(os.path.join(TEST_ARCHIVE_DIR, f))
        os.rmdir(TEST_ARCHIVE_DIR)


def test_archive_file_success():
    # テストファイルを作成
    with open(TEST_FILE, "w") as f:
        f.write("This is a test file.\n")

    cmdline = f"uv run archive_file.py --debug --dstdir {TEST_ARCHIVE_DIR} {TEST_FILE}"
    print()
    print()
    print(f"* cmdline = {cmdline}")

    result = subprocess.run(cmdline.split(), capture_output=True, text=True)

    print()
    print(f"* stdout\n{result.stdout}")
    print(f"* stderr\n{result.stderr}")
    print(f"* returncode = {result.returncode}")
    print()

    assert result.returncode == RESULT_OK

    assert f"Archived '{TEST_FILE}' to " \
           f"'{TEST_ARCHIVE_DIR}/" in result.stdout
    assert not os.path.exists(TEST_FILE)  # 元のファイルは削除されているはず

    # アーカイブディレクトリにファイルが存在することを確認
    archive_files = os.listdir(TEST_ARCHIVE_DIR)
    assert len(archive_files) == 1
    assert TEST_FILE_NAME in archive_files[0]
    assert archive_files[0].endswith("." + TEST_FILE_EXT)


def test_archive_file_set_status():
    # テストファイルを作成
    with open(TEST_FILE, "w") as f:
        f.write("This is a test file.\n")

    cmdline = "uv run archive_file.py --debug"
    cmdline += f" --dstdir {TEST_ARCHIVE_DIR}"
    cmdline += f" --stat {TEST_STAT} {TEST_FILE}"
    print()
    print()
    print(f"* cmdline = {cmdline}")

    result = subprocess.run(cmdline.split(), capture_output=True, text=True)

    print()
    print(f"* stdout\n{result.stdout}")
    print(f"* stderr\n{result.stderr}")
    print(f"* returncode = {result.returncode}")
    print()

    assert result.returncode == RESULT_OK

    assert f"Archived '{TEST_FILE}' to " \
           f"'{TEST_ARCHIVE_DIR}/" in result.stdout
    assert not os.path.exists(TEST_FILE)  # 元のファイルは削除されているはず

    # アーカイブディレクトリにファイルが存在することを確認
    archive_files = os.listdir(TEST_ARCHIVE_DIR)
    assert len(archive_files) == 1
    assert TEST_FILE_NAME in archive_files[0]
    assert archive_files[0].endswith(f"-{TEST_STAT}.{TEST_FILE_EXT}")


def test_file_not_found():
    cmdline = f"uv run archive_file.py --debug --dstdir {TEST_ARCHIVE_DIR} {TEST_FILE_NOTFOUND}"
    print()
    print()
    print(f"* cmdline = {cmdline}")

    result = subprocess.run(cmdline.split(), capture_output=True, text=True)

    print()
    print(f"* stdout\n{result.stdout}")
    print(f"* stderr\n{result.stderr}")
    print(f"* returncode = {result.returncode}")
    print()

    assert result.returncode == RESULT_FILE_NOTFOUND
    assert f"file not found: '{TEST_FILE_NOTFOUND}'" in result.stderr


def test_directory_not_found():
    # テストファイルを作成
    with open(TEST_FILE, "w") as f:
        f.write("This is a test file.\n")

    cmdline = f"uv run archive_file.py --debug --dstdir {TEST_DIR_NOTFOUND} {TEST_FILE}"
    print()
    print()
    print(f"* cmdline = {cmdline}")

    result = subprocess.run(cmdline.split(), capture_output=True, text=True)
    print()
    print(f"* stdout\n{result.stdout}")
    print(f"* stderr\n{result.stderr}")
    print(f"* returncode = {result.returncode}")
    print()

    assert result.returncode == RESULT_DIR_NOTFOUND
    assert f"directory not found: {TEST_DIR_NOTFOUND}/" in result.stderr

    # ファイルを削除
    os.remove(TEST_FILE)
