import sys
import ctypes
from pathlib import Path

import pytest

from TreeGen import (
    FILE_ATTRIBUTE_HIDDEN,
    calculate_folder_size,
    iter_visible_children,
    is_hidden_path,
)

FILE_ATTRIBUTE_DIRECTORY = 0x10


def _set_attributes(path: Path, attributes: int) -> None:
    current = ctypes.windll.kernel32.GetFileAttributesW(str(path))
    if current == 0xFFFFFFFF:
        raise OSError(f"Unable to read attributes for {path}")
    desired = current | attributes
    if not ctypes.windll.kernel32.SetFileAttributesW(str(path), desired):
        raise OSError(f"Unable to set attributes {attributes} on {path}")


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Windows-specific behaviour")
def test_is_hidden_path_detects_windows_hidden_attribute(tmp_path):
    visible_file = tmp_path / "visible.txt"
    visible_file.write_bytes(b"data")

    hidden_file = tmp_path / "hidden.txt"
    hidden_file.write_bytes(b"secret")
    _set_attributes(hidden_file, FILE_ATTRIBUTE_HIDDEN)

    assert not is_hidden_path(visible_file)
    assert is_hidden_path(hidden_file)


@pytest.mark.skipif(not sys.platform.startswith("win"), reason="Windows-specific behaviour")
def test_filters_skip_hidden_and_excluded_entries(tmp_path):
    visible_file = tmp_path / "visible.txt"
    visible_file.write_bytes(b"1234")

    hidden_file = tmp_path / "hidden.txt"
    hidden_file.write_bytes(b"45")
    _set_attributes(hidden_file, FILE_ATTRIBUTE_HIDDEN)

    excluded_log = tmp_path / "ignored.log"
    excluded_log.write_bytes(b"log")

    visible_dir = tmp_path / "visible_dir"
    visible_dir.mkdir()
    (visible_dir / "inner.txt").write_bytes(b"abcd")

    hidden_dir = tmp_path / "hidden_dir"
    hidden_dir.mkdir()
    _set_attributes(hidden_dir, FILE_ATTRIBUTE_DIRECTORY | FILE_ATTRIBUTE_HIDDEN)
    (hidden_dir / "deep.txt").write_bytes(b"hidden")

    children = iter_visible_children(
        tmp_path,
        exclude_hidden=True,
        exclude_extensions=[".log"],
    )
    child_names = {name for name, _, _ in children}

    assert "visible.txt" in child_names
    assert "visible_dir" in child_names
    assert "hidden.txt" not in child_names
    assert "hidden_dir" not in child_names
    assert "ignored.log" not in child_names

    filtered_size = calculate_folder_size(
        tmp_path,
        exclude_hidden=True,
        exclude_extensions=[".log"],
    )
    expected_size = visible_file.stat().st_size + (visible_dir / "inner.txt").stat().st_size

    assert filtered_size == expected_size
