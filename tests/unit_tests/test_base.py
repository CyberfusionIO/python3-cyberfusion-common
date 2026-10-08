import base64
import hashlib
from pathlib import Path

from cyberfusion.Common import (
    download_from_url,
    generate_random_string,
    get_md5_hashes_for_chunks,
)

# download_from_url


def test_download_from_url_custom_root_directory(mock_url: tuple[str, str]) -> None:
    url, _ = mock_url

    assert (
        Path(download_from_url(url, root_directory=str(Path.home()))).parent
        == Path.home()
    )


def test_download_from_url_default_root_directory(mock_url: tuple[str, str]) -> None:
    url, _ = mock_url

    assert Path(download_from_url(url, root_directory=None)).parent == Path("/tmp")


# generate_random_string


def test_generate_random_string_default_length() -> None:
    assert len(generate_random_string()) == 24


def test_generate_random_string_custom_length() -> None:
    length = 8

    assert len(generate_random_string(length=length)) == length


# get_md5_hashes_for_chunks


def test_get_md5_hashes_for_chunks_multiple_chunks(tmp_path: Path) -> None:
    path = tmp_path / "file"
    path.write_bytes(b"abcde")

    assert get_md5_hashes_for_chunks(str(path), chunk_size_bytes=2) == [
        base64.b64encode(hashlib.md5(chunk).digest()).decode("utf-8")
        for chunk in (b"ab", b"cd", b"e")
    ]


def test_get_md5_hashes_for_chunks_single_chunk(tmp_path: Path) -> None:
    path = tmp_path / "file"
    path.write_bytes(b"abcde")

    assert get_md5_hashes_for_chunks(str(path), chunk_size_bytes=1024) == [
        base64.b64encode(hashlib.md5(b"abcde").digest()).decode("utf-8")
    ]


def test_get_md5_hashes_for_chunks_empty_file(tmp_path: Path) -> None:
    path = tmp_path / "file"
    path.write_bytes(b"")

    assert get_md5_hashes_for_chunks(str(path), chunk_size_bytes=2) == []
