import time
import threading
from collections import defaultdict


class MetricsRecorder:
    """
    Thread-safe recorder for capturing latency metrics.
    Stores durations for named events and provides summary statistics.
    """
    def __init__(self):
        self._lock = threading.Lock()
        self._data = defaultdict(list)

    def record(self, name: str, duration: float):
        """
        Record a duration (in seconds) for a given named metric.

        :param name: Identifier for the metric (e.g., 'ws_process_tick')
        :param duration: Duration in seconds
        """
        with self._lock:
            self._data[name].append(duration)

    def get_stats(self, name: str) -> dict:
        """
        Return summary statistics for a metric.

        :param name: Metric name
        :return: Dict with count, min, max, avg, median
        """
        with self._lock:
            vals = self._data.get(name, [])
            if not vals:
                return {'count': 0, 'min': None, 'max': None, 'avg': None, 'median': None}
            sorted_vals = sorted(vals)
            count = len(sorted_vals)
            total = sum(sorted_vals)
            avg = total / count
            median = (sorted_vals[count // 2] if count % 2 == 1
                      else (sorted_vals[count//2 - 1] + sorted_vals[count//2]) / 2)
            return {
                'count': count,
                'min': sorted_vals[0],
                'max': sorted_vals[-1],
                'avg': avg,
                'median': median
            }

    def reset(self, name: str = None):
        """
        Reset recorded data for a specific metric or all metrics.

        :param name: Metric name to reset (if None, reset all)
        """
        with self._lock:
            if name:
                self._data.pop(name, None)
            else:
                self._data.clear()

    @property
    def lock(self):
        return self._lock

    @property
    def data(self):
        return self._data


# Global default recorder
recorder = MetricsRecorder()


class measure:
    """
    Context manager / decorator for measuring execution time and recording it.

    Usage as context manager:
        with measure('ws_process_tick'):
            process_tick()

    Usage as decorator:
        @measure('process_loop')
        def loop():
            ...
    """
    def __init__(self, name: str):
        self.name = name
        self._start = None

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        duration = end - self._start
        recorder.record(self.name, duration)

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            start = time.perf_counter()
            try:
                return func(*args, **kwargs)
            finally:
                end = time.perf_counter()
                recorder.record(self.name, end - start)
        return wrapper


# Async context manager
class AsyncMeasure:
    """
    Async context manager for measuring async function or block.

    Usage:
        async with AsyncMeasure('ws_receive'):
            msg = await ws.recv()
    """
    def __init__(self, name: str):
        self.name = name
        self._start = None

    async def __aenter__(self):
        self._start = time.perf_counter()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        end = time.perf_counter()
        duration = end - self._start
        recorder.record(self.name, duration)


# Utility to report all metrics
def report_all() -> dict:
    """
    Returns summary for all recorded metrics.

    :return: Dict mapping metric names to their stats dict.
    """
    with recorder.lock:
        return {name: recorder.get_stats(name) for name in recorder.data.keys()}
