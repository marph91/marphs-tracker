import time

try:
    # micropython
    START_MS = time.ticks_ms()
except AttributeError:
    # python
    START_MS = time.time() * 1000


class Logger:
    def __init__(self, module):
        self.module = module.upper()

    def __call__(self, message):
        try:
            elapsed_ms = time.ticks_diff(time.ticks_ms(), START_MS)
        except AttributeError:
            elapsed_ms = time.time() * 1000 - START_MS
        print(f"[{elapsed_ms / 1000:6.3f}s - {self.module}] {message}")
