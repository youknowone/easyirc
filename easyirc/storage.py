
from cacheobj.storage import Storage
from cacheobj.backend import BaseBackend
from cacheobj.backend.file import JsonFileBackend

def make_storage(backend, prefix):
    if not isinstance(backend, BaseBackend):
        backend = JsonFileBackend(backend)
    return Storage(backend, prefix)
