import os
from pathlib import Path
from typing import Generator

from cyberfusion.Common import FilesystemComparison
from tests._utilities import traverse_dict


def test_get_different_files_in_directories(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_different_files_in_directories(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 1

    assert comparison[0][0] == os.path.join(
        filesystem_comparison_workspace_directory, "left", "not_identical"
    )
    assert comparison[0][1] == os.path.join(
        filesystem_comparison_workspace_directory, "right", "not_identical"
    )


def test_get_files_only_in_left_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_files_only_in_left_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 1

    assert comparison[0] == os.path.join(
        filesystem_comparison_workspace_directory, "left", "left_only_file"
    )


def test_get_files_only_in_right_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_files_only_in_right_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 1

    assert comparison[0] == os.path.join(
        filesystem_comparison_workspace_directory, "right", "right_only_file"
    )


def test_get_directories_only_in_left_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_directories_only_in_left_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 1

    assert comparison[0] == os.path.join(
        filesystem_comparison_workspace_directory,
        "left",
        "left_only_directory",
    )


def test_get_directories_only_in_right_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_directories_only_in_right_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 1

    assert comparison[0] == os.path.join(
        filesystem_comparison_workspace_directory,
        "right",
        "right_only_directory",
    )


def test_get_nested_directory_structure_different_files_in_directories_left(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = [
        i[0]  # Left
        for i in FilesystemComparison.get_different_files_in_directories(
            os.path.join(filesystem_comparison_workspace_directory, "left"),
            os.path.join(filesystem_comparison_workspace_directory, "right"),
        )
    ]

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"left": {"not_identical": None}}


def test_get_nested_directory_structure_different_files_in_directories_right(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = [
        i[1]  # Right
        for i in FilesystemComparison.get_different_files_in_directories(
            os.path.join(filesystem_comparison_workspace_directory, "left"),
            os.path.join(filesystem_comparison_workspace_directory, "right"),
        )
    ]

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"right": {"not_identical": None}}


def test_get_nested_directory_structure_files_only_in_left_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_files_only_in_left_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"left": {"left_only_file": None}}


def test_get_nested_directory_structure_files_only_in_right_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_files_only_in_right_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"right": {"right_only_file": None}}


def test_get_nested_directory_structure_directories_only_in_left_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_directories_only_in_left_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"left": {"left_only_directory": None}}


def test_get_nested_directory_structure_directories_only_in_right_directory(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    comparison = FilesystemComparison.get_directories_only_in_right_directory(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    nested_directory_structure = (
        FilesystemComparison.get_nested_directory_structure(comparison)
    )

    root = traverse_dict(
        nested_directory_structure,
        Path(filesystem_comparison_workspace_directory).parts,
    )

    assert root == {"right": {"right_only_directory": None}}
