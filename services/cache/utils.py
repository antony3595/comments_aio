import hashlib
from typing import Any


def make_key(*args: Any, **kwargs: Any) -> str:
    args_str = str(args) if args else ""
    kwargs_str = str(sorted(kwargs.items())) if kwargs else ""
    combined = f"{args_str}:{kwargs_str}"
    return hashlib.md5(combined.encode()).hexdigest()
