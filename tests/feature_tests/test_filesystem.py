import os
import sys
from typing import List

import pytest
from psutil._ntuples import sdiskpart
from pytest_mock import MockerFixture

from cyberfusion.Common.Filesystem import (
    FilesystemType,
    get_directory_size,
    get_filesystem,
    get_filesystem_type,
)

BYTES_CEPH = 128021

if sys.platform != "darwin":  # See test_get_directory_size_ceph
    ORIGINAL_GETXATTR = os.getxattr  # type: ignore[attr-defined]


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
        sdiskpart(
            device="[fdb7:b01e:7b8e:0:10:10:10:1],[fdb7:b01e:7b8e:0:10:10:10:2],[fdb7:b01e:7b8e:0:10:10:10:3]:/testpath",
            mountpoint="/mnt/ceph",
            fstype="ceph",
            opts="rw,noatime,name=testuser,secret=<hidden>,acl,readdir_max_entries=32768,readdir_max_bytes=16777216",
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
    reason="os.getxattr does not exist on macOS",
)
def test_get_directory_size_ceph(mocker: MockerFixture) -> None:
    PATH_CEPH = "/mnt/ceph"

    def ismount_side_effect(path: str) -> bool:
        return path == PATH_CEPH

    def getxattr_side_effect(path: str, attribute: str) -> bytes:
        if path == PATH_CEPH and attribute == "ceph.dir.rbytes":
            return str(BYTES_CEPH).encode()

        return ORIGINAL_GETXATTR(path, attribute)

    mocker.patch("os.path.ismount", side_effect=ismount_side_effect)
    mocker.patch(
        "psutil.disk_partitions",
        side_effect=disk_partitions_side_effect,
    )
    mocker.patch("os.getxattr", side_effect=getxattr_side_effect)

    assert get_directory_size(PATH_CEPH) == BYTES_CEPH


def test_get_directory_size_other(mocker: MockerFixture) -> None:
    # We don't know the size, just that it shouldn't be the same as CephFS; so
    # this tests that the branch for the correct filesystem is used

    assert get_directory_size("/tmp") != BYTES_CEPH
