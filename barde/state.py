from typing import Protocol, runtime_checkable
from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


@runtime_checkable
class State(Protocol):
    def to_dict(self) -> dict:
        ...

    @classmethod
    def from_dict(cls, dict_in: dict) -> "State":
        ...


STORAGE = ObjectStorage(storage)
