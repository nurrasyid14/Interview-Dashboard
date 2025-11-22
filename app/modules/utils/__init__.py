# app/modules/utils/__init__.py

"""
Utility module for ID generation, validation, and pipeline orchestration.

Exports:
- generate_user_id: Create formatted user IDs.
- validate_name, validate_username, validate_age, validate_job_specialties
- validate_metadata: One-call metadata validator.
- PipelineBlock, CompositePipeline: Base classes for building pipeline processes.
"""

from .idgen import generate_user_id
from .validators import (
    validate_name,
    validate_username,
    validate_age,
    validate_job_specialties,
    validate_metadata
)
from .pipeline import PipelineBlock, CompositePipeline

__all__ = [
    "generate_user_id",
    "validate_name",
    "validate_username",
    "validate_age",
    "validate_job_specialties",
    "validate_metadata",
    "PipelineBlock",
    "CompositePipeline",
]
