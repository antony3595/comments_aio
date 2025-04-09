import functools
import logging
import pickle
from typing import Callable, TypeVar, Coroutine, Any

from config import settings
from services.cache.service import get_cache_service
from services.cache.utils import make_key

T = TypeVar("T")
AsyncFunc = Callable[..., Coroutine[Any, Any, T]]
WrapperReturnType = AsyncFunc | Callable[..., AsyncFunc]


def acached_wrapper(
    ttl: int,
    key_builder: Callable[..., str] | None = None,
    serializer: Callable[[Any], bytes] = pickle.dumps,
    deserializer: Callable[[bytes], Any] = pickle.loads,
) -> WrapperReturnType:
    def acached_real_decorator(func: AsyncFunc) -> AsyncFunc:
        @functools.wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            if key_builder is None:
                key = func.__qualname__ + make_key(args, kwargs)
            else:
                key = key_builder(*args, **kwargs)
            async with get_cache_service() as cache:
                value = await cache.get(key)
                if value is not None:
                    deserialized_value = deserializer(value)
                    logging.info(f"FROM CACHE {func.__qualname__}[{key}]")
                    return deserialized_value
                else:
                    new_value = await func(*args, **kwargs)
                    new_serialized_value = serializer(new_value)
                    await cache.set(key, new_serialized_value, ex=ttl)
                    logging.info(f"CACHED {func.__qualname__}[{key}]")

                    return new_value

        return wrapper

    return acached_real_decorator


def acached(
    func: AsyncFunc | None = None,
    ttl: int = settings.CACHE_VALUE_DEFAULT_TTL,
    key_builder: Callable[..., str] | None = None,
    serializer: Callable[[Any], bytes] = pickle.dumps,
    deserializer: Callable[[bytes], Any] = pickle.loads,
):
    wrapper = acached_wrapper(ttl, key_builder, serializer, deserializer)
    if func is None:
        return wrapper
    return wrapper(func)
