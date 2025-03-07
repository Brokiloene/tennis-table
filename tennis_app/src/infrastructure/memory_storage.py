import threading
import heapq
from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from tennis_app.src.config import settings


class MemoryStorage:
    """
    LFU cache using UUID keys to access data
    """

    @dataclass(order=True)
    class _FrequencyInfo:
        # in heap instances will be sorted by "frequency" attribute
        frequency: int
        key: UUID = field(compare=False)

        def __repr__(self) -> str:
            return f"frequency: {self.frequency}, key: {str(self.key)[:4]}"

    def __init__(self, capacity: int | None = None):
        self.capacity: int = (
            capacity if capacity is not None else settings.MEMORY_STORAGE_CAPACITY
        )
        self._lock = threading.RLock()

        self._cached_data: dict[UUID, Any] = {}

        # _lfu is a min heap
        self._lfu: list[MemoryStorage._FrequencyInfo] = []

        # _freqs for fast updating without rebuilding the heap
        self._freqs: dict[UUID, MemoryStorage._FrequencyInfo] = {}

    def _evict(self) -> None:
        while len(self._lfu) != 0:
            if len(self._cached_data) < self.capacity:
                return

            freq_info = heapq.heappop(self._lfu)
            # check if freq_info is actual
            if self._freqs[freq_info.key].frequency == freq_info.frequency:
                del self._freqs[freq_info.key]

                if freq_info.key in self._cached_data:
                    del self._cached_data[freq_info.key]
            else:
                continue

    def _update_frequency(self, key) -> None:
        freq_info = self._freqs[key]
        freq_info.frequency += 1
        heapq.heappush(self._lfu, self._FrequencyInfo(freq_info.frequency, key))

    def put(self, key: UUID, value: Any) -> None:
        with self._lock:
            if len(self._cached_data) >= self.capacity:
                self._evict()

            self._freqs[key] = self._FrequencyInfo(0, key)
            heapq.heappush(self._lfu, self._freqs[key])
            self._cached_data[key] = value

    def get_value(self, key: UUID) -> Any:
        """
        :raises: KeyError
        """
        with self._lock:
            if key not in self._cached_data:
                raise KeyError(key)
            self._update_frequency(key)
            return self._cached_data[key]

    def update_value(self, key: UUID, new_value: Any) -> None:
        """
        :raises: KeyError
        """
        with self._lock:
            if key not in self._cached_data:
                raise KeyError(key)
            self._cached_data[key] = new_value
            self._update_frequency(key)

    def delete(self, key: UUID) -> None:
        """
        :raises: KeyError
        """
        with self._lock:
            if key not in self._cached_data:
                raise KeyError(key)
            # make freq_info outdated so it will be deleted on _evict() call
            freq_info = self._freqs[key]
            freq_info.frequency += 1
            del self._cached_data[freq_info.key]

    def __repr__(self) -> str:
        return (
            f"Capacity: {self.capacity} Cache: {self._cached_data} Freqs: {self._freqs}"
        )
