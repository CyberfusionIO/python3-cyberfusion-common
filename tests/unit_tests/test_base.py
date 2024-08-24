from pathlib import Path

from cyberfusion.Common import download_from_url, generate_random_string

# download_from_url


def test_download_from_url_custom_root_directory() -> None:
    assert (
        Path(
            download_from_url("https://example.com", root_directory=str(Path.home()))
        ).parent
        == Path.home()
    )


def test_download_from_url_default_root_directory() -> None:
    assert Path(
        download_from_url("https://example.com", root_directory=None)
    ).parent == Path("/tmp")


# generate_random_string


def test_generate_random_string_default_length() -> None:
    assert len(generate_random_string()) == 24


def test_generate_random_string_custom_length() -> None:
    length = 8

    assert len(generate_random_string(length=length)) == length
