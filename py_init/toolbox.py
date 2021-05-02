import subprocess
import shutil
import os
import stat
from py_init.setup_exception import SetupException


def append_to_file(file_path: str, string_to_append: str) -> None:
    f = open(file_path, "a")
    f.write(f"{string_to_append}\n")
    f.close()


def check_and_append_to_file(file_path: str, string_to_append: str) -> None:
    # appending string if not already exists

    if not check_string_in_file(file_path, string_to_append):
        append_to_file(file_path, string_to_append)


def check_string_in_file(file_path: str, string_to_check: str) -> bool:
    f = open(file_path, "r")
    string_found = False
    for line in f:
        stripped_line = line.strip()
        if stripped_line == string_to_check:
            string_found = True
    f.close()

    return string_found


def read_from_file(file_path: str) -> str:
    f = open(file_path, "r")
    file_content = ""
    for line in f:
        stripped_line = line.strip()
        file_content += f"{stripped_line}\n"
    f.close()
    return file_content


def write_to_file(file_path: str, string_to_write: str) -> None:
    f = open(file_path, "w")
    f.write(f"{string_to_write}\n")
    f.close()


def replace_string_in_file(
    file_path: str, string_to_replace: str, new_string: str
) -> None:
    # get file content, iterate and replace
    f = open(file_path, "r")
    new_file_content = ""
    for line in f:
        stripped_line = line.strip()
        new_line = stripped_line.replace(string_to_replace, new_string)
        new_file_content += f"{new_line}\n"
    f.close()

    # write new file content to file
    f = open(file_path, "w")
    f.write(new_file_content)
    f.close()


def call_bash_command(command: str) -> str:
    output = subprocess.run(
        ["/bin/bash", "-c", command], capture_output=True, text=True
    )
    if output.returncode == 0:
        return output.stdout
    else:
        raise SetupException(output.stderr)


def copy_file(source_path: str, destination_path: str) -> None:
    shutil.copy2(source_path, destination_path)


def copy_directory(source_path: str, destination_path: str) -> None:
    shutil.copytree(source_path, destination_path)


def make_executable(file_path: str) -> None:
    st = os.stat(file_path)
    os.chmod(file_path, st.st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)


def file_exists(file_path: str) -> bool:
    return os.path.isfile(file_path)


def get_file_size(file_path: str) -> int:
    return os.path.getsize(file_path)
