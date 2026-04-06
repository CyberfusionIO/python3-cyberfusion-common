from pathlib import PosixPath
from typing import List
import faker
import pytest
from psutil._ntuples import sdiskpart
from pytest_mock import MockerFixture

from cyberfusion.Common.Filesystem import (
    FilesystemType,
    get_directory_size,
    get_filesystem,
    get_filesystem_type,
)
import sys


def disk_partitions_side_effect(all: bool = False) -> List[sdiskpart]:
    return [
        sdiskpart(
            device="/dev/mapper/sandbox--vg-root",
            mountpoint="/",
            fstype="ext4",
            opts="rw,relatime,errors=remount-ro",
        ),
        sdiskpart(
            device="/dev/sda1",
            mountpoint="/boot",
            fstype="ext2",
            opts="rw,relatime",
        ),
    ]


def test_get_filesystem(mocker: MockerFixture) -> None:
    def ismount_side_effect(path: str) -> bool:
        return path == "/var"

    mocker.patch("os.path.ismount", side_effect=ismount_side_effect)

    assert get_filesystem("/var/run/test") == "/var"


def test_get_filesystem_type_exists(mocker: MockerFixture) -> None:
    mocker.patch(
        "psutil.disk_partitions",
        side_effect=disk_partitions_side_effect,
    )

    assert get_filesystem_type("/") == FilesystemType.EXT4


def test_get_filesystem_type_not_exists(mocker: MockerFixture) -> None:
    mocker.patch(
        "psutil.disk_partitions",
        side_effect=disk_partitions_side_effect,
    )

    with pytest.raises(StopIteration):
        get_filesystem_type("/tmp")


@pytest.mark.skipif(
    sys.platform == "darwin",
    reason="`-b` doesn't exist on BSD du",
)
def test_get_directory_size(
    mocker: MockerFixture, tmp_path: PosixPath, faker: faker.Faker
) -> None:
    string = faker.word()

    with open(tmp_path / "test.txt", "w") as f:
        f.write(string)

    assert get_directory_size(str(tmp_path)) == len(string.encode())
