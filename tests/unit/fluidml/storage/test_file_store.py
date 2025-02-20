import tempfile

import pytest

from fluidml.storage import LocalFileStore, ResultsStore


@pytest.fixture
def file_store():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_store = LocalFileStore(base_dir=temp_dir)
        yield file_store


def test_first_load(file_store: ResultsStore):
    loaded_obj = file_store.load("dummy_item", "dummy_task", {})
    assert loaded_obj is None


@pytest.mark.parametrize("type_", ["json", "pickle"])
def test_save_load(file_store: ResultsStore, type_: str):
    test_item_name = "dummy_item"
    test_task_name = "dummy_task"
    test_json_obj = {"dummy_result": "test"}
    test_config = {"config_param": 1}

    file_store.save(
        obj=test_json_obj,
        name=test_item_name,
        type_=type_,
        task_name=test_task_name,
        task_unique_config=test_config,
    )
    loaded_json_obj = file_store.load(
        name=test_item_name, task_name=test_task_name, task_unique_config=test_config
    )
    assert loaded_json_obj == test_json_obj
