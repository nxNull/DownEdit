import asyncio
import time
import traceback
import httpx

from decorator import decorator
from downedit.utils import log


@decorator
async def retry_async(
    func,
    *args,
    num_retries=3,
    delay=1,
    exceptions=(Exception,),
    **kwargs
):
    """
    Retry decorator.

    Args:
        func (callable): The function to wrap.
        num_retries (int, optional): Number of retries. Defaults to 3.
        delay (int, optional): Delay between retries in seconds. Defaults to 1.
        exceptions (tuple, optional): Exceptions to catch. Defaults to (Exception,).
    """
    last_err: Exception | None = None
    for attempt in range(num_retries):
        try:
            return await func(*args, **kwargs)
        except exceptions as err:
            last_err = err
            if attempt < num_retries - 1:
                await asyncio.sleep(delay)
    raise last_err


@decorator
async def httpx_capture_async(func, *args, **kwargs):
    """
    Capture error decorator.

    Args:
        func (callable): The function to wrap.
    """
    try:
        return await func(*args, **kwargs)
    except (
        httpx.TimeoutException,
        httpx.NetworkError,
        httpx.HTTPStatusError,
        httpx.ProxyError,
        httpx.UnsupportedProtocol,
        httpx.StreamError,
        Exception,
    ) as e:
        log.error(traceback.format_exc())
        log.pause()
        raise


@decorator
def retry_sync(
    func,
    *args,
    num_retries=3,
    delay=1,
    exceptions=(Exception,),
    **kwargs
):
    """
    Retry decorator for sync functions.

    Args:
        func (callable): The sync function to wrap.
        num_retries (int, optional): Number of retries. Defaults to 3.
        delay (int, optional): Delay between retries in seconds. Defaults to 1.
        exceptions (tuple, optional): Exceptions to catch. Defaults to (Exception,).
    """
    for attempt in range(num_retries):
        try:
            result = func(*args, **kwargs)
            if result is not None:
                return result
        except exceptions as e:
            # log.error(traceback.format_exc())
            if attempt < num_retries - 1:
                time.sleep(delay)
    return None


@decorator
def httpx_capture_sync(func, *args, **kwargs):
    """
    Capture error decorator for sync functions using httpx.

    Args:
        func (callable): The sync function to wrap.
    """
    try:
        return func(*args, **kwargs)
    except (
        httpx.TimeoutException,
        httpx.NetworkError,
        httpx.HTTPStatusError,
        httpx.ProxyError,
        httpx.UnsupportedProtocol,
        httpx.StreamError,
        Exception,
    ) as e:
        log.error(traceback.format_exc())
        log.pause()
        raise