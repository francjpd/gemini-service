"""Vertex AI model resource helpers.

A Vertex AI model is addressed by a fully-qualified resource path:

    projects/{project}/locations/{location}/publishers/google/models/{model}

Keeping the string in one place means a typo fails in a unit test rather than
in a billed API call six days from now.
"""

from __future__ import annotations

import re

RESOURCE_RE = re.compile(
    r"^projects/(?P<project>[^/]+)/locations/(?P<location>[^/]+)"
    r"/publishers/google/models/(?P<model>[^/]+)$"
)


def model_resource_path(project: str, location: str, model: str) -> str:
    """Return the fully-qualified Vertex AI model resource path.

    Raises:
        ValueError: if any part is empty, or ``model`` contains a slash
            (which would silently produce a malformed path).
    """
    if not project:
        raise ValueError("project must be non-empty")
    if not location:
        raise ValueError("location must be non-empty")
    if not model:
        raise ValueError("model must be non-empty")
    if "/" in model:
        raise ValueError("model must not contain a slash")
    return f"projects/{project}/locations/{location}/publishers/google/models/{model}"


def parse_model_resource(resource: str) -> dict[str, str]:
    """Split a model resource path back into its parts.

    Raises:
        ValueError: if ``resource`` is not a valid model resource path.
    """
    match = RESOURCE_RE.match(resource)
    if not match:
        raise ValueError(f"not a model resource path: {resource!r}")
    return match.groupdict()
