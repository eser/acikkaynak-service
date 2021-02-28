import os

from .env_file import EnvFile


def find_env_dir():
    raise NotImplementedError


def load_env(dir_path=None, environment_mode_variable="PYTHON_ENV", auto_parse=True):
    dir_path = dir_path or find_env_dir()
    environment_mode = os.environ.get(environment_mode_variable, "development").lower()

    file_hierarchy = (
        f".env.{environment_mode}.local",
        ".env.local",
        f".env.{environment_mode}",
        ".env",
    )

    env_file = EnvFile(auto_parse=auto_parse)

    # environment variables first
    data = dict(os.environ)
    env_file.update(data)

    # then the file hierarchy
    for file in file_hierarchy:
        file_path = os.path.join(dir_path, file)

        try:
            data = _read_file(file_path)
            env_file.update(data)
        except FileNotFoundError:
            pass

    env_file.export()

    return env_file


def _read_file(file_path):
    output = {}

    with open(file_path, "r") as file:
        for raw_line in file.readlines():
            line = raw_line.split("#")[0].rstrip()

            if "=" in line:
                key, value = line.split("=")
                output[key] = value

    return output
