# -*- coding: utf-8 -*-

from json import load
from pathlib import Path

import pytest

from redox.factory import get_class_type, redox_object_factory

# noinspection PyPackageRequirements
from retry import retry

SAMPLES_DIR = (Path(__file__).parent / "fixtures").resolve()

REDOX_LIB_DIR = (Path(__file__).parent.parent / "redox").resolve()
SAMPLE_DATA_FILE_PATH = [
    (Path(f"{module.name}_{event.stem.lower()}.json"),)
    for module in REDOX_LIB_DIR.iterdir()
    if module.is_dir() and module.name != "generic" and not module.name.startswith("_")
    for event in module.iterdir()
    if not event.name.startswith("_")
]
SKIP_FILES = [
    str(SAMPLES_DIR / f)
    for f in [
        # "clinicaldecisions_request.json",
    ]
]


@pytest.mark.parametrize(
    ("json_file_path",),
    SAMPLE_DATA_FILE_PATH,
    ids=[str(p[0]) for p in SAMPLE_DATA_FILE_PATH],
)
@retry(FileNotFoundError, tries=3, delay=1, backoff=1.5)
def test_json_redox_json(json_file_path: Path):
    current_sample_path = SAMPLES_DIR / json_file_path
    assert current_sample_path.exists
    try:
        with open(current_sample_path) as sample_fd:
            sample = load(sample_fd)
    except FileNotFoundError as err:
        if err.filename in SKIP_FILES:
            return
        raise

    expected_type = get_class_type(sample)
    obj = expected_type(**sample)
    assert isinstance(obj, expected_type)
    assert sample == obj.model_dump()


@pytest.mark.parametrize(
    ("json_file_path",),
    SAMPLE_DATA_FILE_PATH,
    ids=[str(p[0]) for p in SAMPLE_DATA_FILE_PATH],
)
@retry(FileNotFoundError, tries=3, delay=1, backoff=1.5)
def test_redox_factory(json_file_path: Path):
    current_sample_path = SAMPLES_DIR / json_file_path
    assert current_sample_path.exists
    try:
        with open(current_sample_path) as sample_fd:
            sample = load(sample_fd)
    except FileNotFoundError as err:
        if err.filename in SKIP_FILES:
            return
        raise

    expected_type = get_class_type(sample)
    obj = redox_object_factory(sample)
    assert isinstance(obj, expected_type)
    assert sample == obj.model_dump()
