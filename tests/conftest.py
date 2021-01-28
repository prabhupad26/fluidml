from dataclasses import dataclass
from typing import Dict

import pytest

from fluidml.common import Task, Resource


class DummyTaskA(Task):
    def __init__(self, x: int):
        super().__init__()

    def run(self):
        self.save(obj={'a': 1}, name='a', type_='json')


class DummyTaskB(Task):
    def __init__(self, x: int):
        super().__init__()

    def run(self, a: Dict):
        self.save(obj={'b': 1}, name='b', type_='json')


@pytest.fixture
def dummy_task_a():
    return DummyTaskA


@pytest.fixture
def dummy_task_b():
    return DummyTaskB


@dataclass
class TaskResource(Resource):
    seed: int


@pytest.fixture
def dummy_resource():
    return TaskResource
