from typing import Any, Protocol, runtime_checkable
from browser.local_storage import storage  # type:ignore # pylint: disable=import-error
from browser.object_storage import (  # type:ignore # pylint: disable=import-error
    ObjectStorage,
)


@runtime_checkable
class State(Protocol):
    def to_dict(self) -> dict[str, Any]:
        ...

    @classmethod
    def from_dict(cls, dict_in: dict[str, Any]) -> "State":
        ...


STORAGE = ObjectStorage(storage)
