import os

import pytest

from cyberfusion.Common import (
    convert_bytes_gib,
    download_from_url,
    find_executable,
    generate_random_string,
    get_domain_is_wildcard,
    get_hostname,
    get_md5_hash,
    get_tmp_file,
    get_today_timestamp,
    hash_string_mariadb,
    try_find_executable,
    ensure_trailing_newline,
)
from cyberfusion.Common.exceptions import ExecutableNotFound

# find_executable


def test_find_executable_found() -> None:
    assert find_executable("true")


def test_find_executable_not_found() -> None:
    with pytest.raises(ExecutableNotFound) as e:
        find_executable("doesnotexist")

    assert e.value.name == "doesnotexist"


# try_find_executable


def test_try_find_executable_found() -> None:
    assert try_find_executable("true") is not None


def test_try_find_executable_not_found() -> None:
    assert try_find_executable("doesnotexist") is None


# download_from_url


def test_download_from_url(mock_url: tuple[str, str]) -> None:
    url, text = mock_url

    path = download_from_url(url)

    assert os.path.isfile(path)
    assert open(path, "r").read() == text
    assert os.stat(path).st_mode == 33152


# get_tmp_file


def test_get_tmp_file() -> None:
    path = get_tmp_file()

    assert path.startswith("/tmp/")
    assert os.stat(path).st_mode == 33152


# get_hostname


def test_get_hostname() -> None:
    assert isinstance(get_hostname(), str)


# get_domain_is_wildcard


def test_get_domain_is_wildcard_not_wildcard() -> None:
    assert not get_domain_is_wildcard("test.nl")
    assert not get_domain_is_wildcard("www.test.nl")
    assert not get_domain_is_wildcard("*test.nl")
    assert not get_domain_is_wildcard("test.*.nl")


def test_get_domain_is_wildcard_wildcard() -> None:
    assert get_domain_is_wildcard("*.test.nl")
    assert get_domain_is_wildcard("*.www.test.nl")


# generate_random_string


def test_generate_random_string() -> None:
    assert isinstance(generate_random_string(), str)


# get_today_timestamp


def test_get_today_timestamp() -> None:
    assert isinstance(get_today_timestamp(), float)


# hash_string_mariadb


def test_hash_string_mariadb() -> None:
    assert (
        hash_string_mariadb(string="test")
        == "*94BDCEBE19083CE2A1F959FD02F964C7AF4CFC29"
    )


# convert_bytes_gib


def test_convert_bytes_gib() -> None:
    assert convert_bytes_gib(5905580032) == 5.5


# get_md5_hash


def test_get_md5_hash() -> None:
    assert get_md5_hash("large_file.zip") == "c14liqPHO4T8t8bGUbpWMw=="


# ensure_trailing_newline


def test_ensure_trailing_newline_added() -> None:
    CONTENTS = "test"

    assert ensure_trailing_newline(CONTENTS) == CONTENTS + "\n"


def test_ensure_trailing_newline_present() -> None:
    CONTENTS = "test\n"

    assert ensure_trailing_newline(CONTENTS) == CONTENTS
