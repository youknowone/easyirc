
from easyirc.storage import make_storage


def test_storage():
    storage = make_storage('test.json', 'test')
    storage._del_foo()
    assert storage.foo == None
    storage.foo = 'bar'
    assert storage.foo == 'bar'
    storage = make_storage('test.json', 'test')
    assert storage.foo == 'bar'