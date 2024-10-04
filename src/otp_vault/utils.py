# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.


# Future Modules:
from __future__ import annotations

# Built-in Modules:
import _imp
import os
import sys
from typing import Union


DATA_DIRECTORY: str = "otp_vault_data"


def get_freezer() -> Union[str, None]:
	"""
	Determines the name of the library used to freeze the code.

	Note:
		https://github.com/blackmagicgirl/ktools/blob/master/ktools/utils.py

	Returns:
		The name of the library or None.
	"""
	frozen: Union[str, bool, None] = getattr(sys, "frozen", None)
	if frozen and hasattr(sys, "_MEIPASS"):
		return "pyinstaller"
	if frozen is True:
		return "cx_freeze"
	if frozen in ("windows_exe", "console_exe", "dll"):
		return "py2exe"
	if frozen == "macosx_app":
		return "py2app"
	if hasattr(sys, "importers"):
		return "old_py2exe"
	if _imp.is_frozen("__main__"):
		return "tools/freeze"
	if isinstance(frozen, str):
		return f"unknown {frozen}"
	return None


def is_frozen() -> bool:
	"""
	Determines whether the program is running from a frozen copy or from source.

	Returns:
		True if frozen, False otherwise.
	"""
	return bool(get_freezer())


def get_directory_path(*args: str) -> str:
	"""
	Retrieves the path of the directory where the program is located.

	Args:
		*args: Positional arguments to be passed to os.join after the directory path.

	Returns:
		The path.
	"""
	if is_frozen():
		path = os.path.dirname(sys.executable)
	else:
		path = os.path.join(os.path.dirname(__file__), os.path.pardir)
	return os.path.realpath(os.path.join(path, *args))


def get_data_path(*args: str) -> str:
	"""
	Retrieves the path of the data directory.

	Args:
		*args: Positional arguments to be passed to os.join after the data path.

	Returns:
		The path.
	"""
	return os.path.realpath(os.path.join(get_directory_path(DATA_DIRECTORY), *args))
