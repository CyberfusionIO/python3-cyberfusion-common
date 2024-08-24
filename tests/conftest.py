import os
import shutil
import uuid
from typing import Generator

import pytest


@pytest.fixture
def filesystem_comparison_workspace_directory() -> Generator[str, None, None]:
    path = os.path.join(os.path.sep, "tmp", str(uuid.uuid4()))

    os.mkdir(path)

    # Create left and right directories

    left_directory = os.path.join(path, "left")
    right_directory = os.path.join(path, "right")

    os.mkdir(left_directory)
    os.mkdir(right_directory)

    # Write identical file

    left_identical_file = os.path.join(left_directory, "identical")
    right_identical_file = os.path.join(right_directory, "identical")

    with open(left_identical_file, "w") as f:
        f.write("Hi!")

    with open(right_identical_file, "w") as f:
        f.write("Hi!")

    # Write not identical file

    left_not_identical_file = os.path.join(left_directory, "not_identical")
    right_not_identical_file = os.path.join(right_directory, "not_identical")

    with open(left_not_identical_file, "w") as f:
        f.write("Hoi")

    with open(right_not_identical_file, "w") as f:
        f.write("Hallo")

    # Write only left or right files

    left_only_file = os.path.join(left_directory, "left_only_file")
    right_only_file = os.path.join(right_directory, "right_only_file")

    with open(left_only_file, "w") as f:
        pass

    with open(right_only_file, "w") as f:
        pass

    # Create only left or right directories

    left_only_directory = os.path.join(left_directory, "left_only_directory")
    right_only_directory = os.path.join(right_directory, "right_only_directory")

    os.mkdir(left_only_directory)
    os.mkdir(right_only_directory)

    yield path

    shutil.rmtree(path)
