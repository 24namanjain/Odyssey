from typing import List, Generator, TypeVar

T = TypeVar('T')

def chunk_list(data: List[T], chunk_size: int = 100) -> Generator[List[T], None, None]:
    """
    Yields successive blocks of a specified size from a list.
    Useful for Notion API limits (e.g. 100 blocks per request).
    """
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]
