import os
from typing import Generator

from cyberfusion.Common import FilesystemComparison


def test_get_different_files_in_directories_with_recursive_dircmps(
    filesystem_comparison_workspace_directory: Generator[str, None, None]
) -> None:
    # Test _get_recursive_dircmps with get_different_files_in_directories (could
    # be any other function)

    os.mkdir(
        os.path.join(
            filesystem_comparison_workspace_directory, "left", "common_dir"
        )
    )
    os.mkdir(
        os.path.join(
            filesystem_comparison_workspace_directory, "right", "common_dir"
        )
    )

    with open(
        os.path.join(
            filesystem_comparison_workspace_directory,
            "left",
            "common_dir",
            "not_identical",
        ),
        "w",
    ) as f:
        f.write("Hola")

    with open(
        os.path.join(
            filesystem_comparison_workspace_directory,
            "right",
            "common_dir",
            "not_identical",
        ),
        "w",
    ) as f:
        f.write("Hey")

    comparison = FilesystemComparison.get_different_files_in_directories(
        os.path.join(filesystem_comparison_workspace_directory, "left"),
        os.path.join(filesystem_comparison_workspace_directory, "right"),
    )

    assert len(comparison) == 2

    assert comparison[0][0] == os.path.join(
        filesystem_comparison_workspace_directory, "left", "not_identical"
    )
    assert comparison[0][1] == os.path.join(
        filesystem_comparison_workspace_directory, "right", "not_identical"
    )
    assert comparison[1][0] == os.path.join(
        filesystem_comparison_workspace_directory,
        "left",
        "common_dir",
        "not_identical",
    )
    assert comparison[1][1] == os.path.join(
        filesystem_comparison_workspace_directory,
        "right",
        "common_dir",
        "not_identical",
    )
