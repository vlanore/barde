from browser.local_storage import storage  # type:ignore ; pylint: disable=import-error
from browser.object_storage import (  # type:ignore ; pylint: disable=import-error
    ObjectStorage,
)


STORAGE = ObjectStorage(storage)
