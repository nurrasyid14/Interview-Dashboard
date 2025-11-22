# app/modules/auth/__init__.py

"""
Authentication + metadata handling module.

Exports:
- build_metadata, save_metadata
- extract_initials
- empty_metadata_template
- login, user_exists, get_user_metadata
"""

from .metadata_filler import (
    build_metadata,
    save_metadata,
    extract_initials
)

from .table_templater import empty_metadata_template

from .login import (
    login,
    user_exists,
    get_user_metadata
)

__all__ = [
    "build_metadata",
    "save_metadata",
    "extract_initials",
    "empty_metadata_template",
    "login",
    "user_exists",
    "get_user_metadata",
]
