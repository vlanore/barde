from typing import Callable, Optional
from browser import document

_passages = {}

_state = {}

_start: Optional[str] = None


def passage(start=False):
    def result(func: Callable):
        global _start
        global _passages
        if start:
            _start = func.__name__
        _passages[func.__name__] = func
        return func

    return result


def run():
    if _start is not None:
        _passages[_start]()


if __name__ == "__main__":

    @passage(start=True)
    def hello():
        document <= "Hello"

    run()
