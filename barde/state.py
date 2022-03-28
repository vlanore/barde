import dataclasses
import json
from typing import Any

from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


class DataClassJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if dataclasses.is_dataclass(o):
            return dataclasses.asdict(o)
        return super().default(o)


def encode_state(state: Any) -> str:
    return json.dumps(state, cls=DataClassJSONEncoder)


STORAGE = ObjectStorage(storage)
