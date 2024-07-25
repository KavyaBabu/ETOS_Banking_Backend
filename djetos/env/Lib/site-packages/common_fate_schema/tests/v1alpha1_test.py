from pathlib import Path
import json
import pytest
from common_fate_schema.provider import v1alpha1
from syrupy.extensions.json import JSONSnapshotExtension
from syrupy.location import PyTestLocation
from syrupy.types import SnapshotIndex


class SchemaOutputExtension(JSONSnapshotExtension):
    _file_extension = ""

    @classmethod
    def dirname(cls, *, test_location: "PyTestLocation") -> str:
        return str(
            Path(test_location.filepath).parent.parent.parent.joinpath(
                "output/provider"
            )
        )

    @classmethod
    def get_snapshot_name(
        cls, *, test_location: "PyTestLocation", index: "SnapshotIndex"
    ) -> str:
        original_name = JSONSnapshotExtension.get_snapshot_name(
            test_location=test_location, index=index
        )
        return original_name.removeprefix("test_")


@pytest.fixture
def export_schema(snapshot):
    return snapshot.use_extension(SchemaOutputExtension)


@pytest.fixture
def snapshot_json(snapshot):
    """use JSON, rather than AmberSnapshotExtension as our schema is serialized as JSON"""
    return snapshot.use_extension(JSONSnapshotExtension)


def test_v1alpha1(export_schema):
    schema_str = v1alpha1.Schema.schema_json()
    actual = json.loads(schema_str)
    assert actual == export_schema


def test_v1alpha1_example(snapshot_json):
    schema = v1alpha1.Schema(
        id=v1alpha1.ID(
            schema_version="v1",
            name="example",
            publisher="common-fate",
        ),
        targets={
            "Group": v1alpha1.Target(
                type="object", properties={"value": v1alpha1.TargetField(type="string")}
            )
        },
        config={"api_url": v1alpha1.Config(type="string", secret=False)},
        meta=v1alpha1.Meta(framework="dev"),
        resources=v1alpha1.Resources(
            loaders={"example": v1alpha1.Loader(title="example")},
            types={"MyResource": {"type": "string"}},
        ),
    )

    assert schema.dict() == snapshot_json


def test_v1alpha1_example_no_provider(snapshot_json):
    schema = v1alpha1.Schema(
        targets={
            "Group": v1alpha1.Target(
                type="object", properties={"value": v1alpha1.TargetField(type="string")}
            )
        },
        config={"api_url": v1alpha1.Config(type="string", secret=False)},
        meta=v1alpha1.Meta(framework="dev"),
        resources=v1alpha1.Resources(
            loaders={"example": v1alpha1.Loader(title="example")},
            types={"MyResource": {"type": "string"}},
        ),
    )

    assert schema.dict() == snapshot_json


def test_v1alpha1_minimal(snapshot_json):
    schema = v1alpha1.Schema(
        meta=v1alpha1.Meta(framework="dev"),
    )

    assert schema.dict(exclude_none=True) == snapshot_json
