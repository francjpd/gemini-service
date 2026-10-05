import pytest

from gemini_service.vertex import model_resource_path, parse_model_resource

RESOURCE = (
    "projects/acme/locations/europe-west4/publishers/google/models/gemini-2.0-flash"
)


def test_builds_a_known_resource_path():
    assert model_resource_path("acme", "europe-west4", "gemini-2.0-flash") == RESOURCE


def test_round_trips_back_to_its_parts():
    assert parse_model_resource(RESOURCE) == {
        "project": "acme",
        "location": "europe-west4",
        "model": "gemini-2.0-flash",
    }


@pytest.mark.parametrize(
    ("project", "location", "model", "message"),
    [
        ("", "europe-west4", "gemini-2.0-flash", "project must be non-empty"),
        ("acme", "", "gemini-2.0-flash", "location must be non-empty"),
        ("acme", "europe-west4", "", "model must be non-empty"),
        ("acme", "europe-west4", "google/gemini", "model must not contain a slash"),
    ],
)
def test_rejects_invalid_parts(project, location, model, message):
    with pytest.raises(ValueError, match=message):
        model_resource_path(project, location, model)


def test_rejects_a_malformed_resource():
    with pytest.raises(ValueError, match="not a model resource path"):
        parse_model_resource("europe-west4")
