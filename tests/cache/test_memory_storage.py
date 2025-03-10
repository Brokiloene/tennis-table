import threading
import uuid

import pytest

from tennis_app.src.infrastructure.memory_storage import MemoryStorage


@pytest.fixture
def memory_storage(request: pytest.FixtureRequest) -> MemoryStorage:
    capacity = getattr(request, "param", None)
    return MemoryStorage(capacity=capacity)


def test_crud(memory_storage: MemoryStorage):
    # create
    key1 = uuid.uuid4()
    memory_storage.put(key1, "value1")

    key2 = uuid.uuid4()
    memory_storage.put(key2, "value2")

    fake_key = uuid.uuid4()

    # read
    assert memory_storage.get_value(key1) == "value1"
    assert memory_storage.get_value(key2) == "value2"
    with pytest.raises(KeyError):
        memory_storage.get_value(fake_key)

    # update
    memory_storage.update_value(key1, "value1.1")
    memory_storage.update_value(key2, "value2.1")

    assert memory_storage.get_value(key1) == "value1.1"
    assert memory_storage.get_value(key2) == "value2.1"

    with pytest.raises(KeyError):
        memory_storage.update_value(fake_key, "")

    # delete
    memory_storage.delete(key1)
    memory_storage.delete(key2)

    with pytest.raises(KeyError):
        memory_storage.get_value(key1)

    with pytest.raises(KeyError):
        memory_storage.get_value(key1)

    with pytest.raises(KeyError):
        memory_storage.delete(fake_key)


@pytest.mark.parametrize(
    "memory_storage",
    [
        3,
    ],
    indirect=True,
)
def test_lfu_cache_logic(memory_storage: MemoryStorage):
    key1 = uuid.uuid4()
    key2 = uuid.uuid4()
    key3 = uuid.uuid4()

    memory_storage.put(key1, "value1")
    memory_storage.put(key2, "value2")
    memory_storage.put(key3, "value3")

    for _ in range(1):
        memory_storage.get_value(key1)
    for _ in range(2):
        memory_storage.get_value(key2)
    for _ in range(3):
        memory_storage.get_value(key3)
    # Now the value with key1 is the least frequent used
    # and will be deleted on exceeding of capacity of the cache

    key4 = uuid.uuid4()
    memory_storage.put(key4, "value4")
    assert memory_storage.get_value(key4) == "value4"

    with pytest.raises(KeyError):
        memory_storage.get_value(key1)


@pytest.mark.slow
def test_race_condition(memory_storage: MemoryStorage):
    NUMBER_OF_UPDATES = 100000

    def change_value_not_atomic(key):
        for _ in range(NUMBER_OF_UPDATES):
            # a non atomic operation
            int(1)
            memory_storage.update_value(key, "a new value")

    key = uuid.uuid4()
    memory_storage.put(key, "value")
    t1 = threading.Thread(target=change_value_not_atomic, args=(key,))
    t2 = threading.Thread(target=change_value_not_atomic, args=(key,))
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert memory_storage.get_value(key) == "a new value"
    # +1 because initial value of frequency is 1
    assert memory_storage._freqs[key].frequency == NUMBER_OF_UPDATES * 2 + 1
