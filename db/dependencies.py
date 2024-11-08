from litestar.di import Provide

from litestar.params import Parameter
from litestar.repository.filters import LimitOffset

from advanced_alchemy.filters import (
    LimitOffset,
    SearchFilter,
)

def provide_limit_offset_pagination(
    current_page: int = Parameter(ge=1, query="currentPage", default=1, required=False),
    page_size: int = Parameter(
        query="pageSize",
        ge=1,
        default=10,
        required=False,
    )
) -> LimitOffset:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_limit_offset_pagination()`.

    Parameters
    ----------
    current_page : int
        LIMIT to apply to select.
    page_size : int
        OFFSET to apply to select.
    """
    return LimitOffset(page_size, page_size * (current_page - 1))



def provide_search_filter(
    field: str | None = Parameter(title="Field to search", query="searchField", default=None, required=False),
    search: str | None = Parameter(title="Field to search", query="searchString", default=None, required=False),
    ignore_case: bool | None = Parameter(
        title="Search should be case sensitive",
        query="searchIgnoreCase",
        default=None,
        required=False,
    ),
) -> SearchFilter:
    """Add offset/limit pagination.

    Return type consumed by `Repository.apply_search_filter()`.

    Args:
        field (StringOrNone): Field name to search.
        search (StringOrNone): Value to search for.
        ignore_case (BooleanOrNone): Whether to ignore case when searching.

    Returns:
        SearchFilter: Filter for searching fields.
    """
    return SearchFilter(field_name=field, value=search, ignore_case=ignore_case or False)  # type: ignore[arg-type]



def create_collection_dependencies() -> dict[str, Provide]:
    """Create ORM dependencies.

    Creates a dictionary of provides for pagination endpoints.

    Returns:
        dict[str, Provide]: Dictionary of provides for pagination endpoints.
    """ 
    return {
        "limit_offset": Provide(provide_limit_offset_pagination, sync_to_thread=False),
        "search_filter": Provide(provide_search_filter, sync_to_thread=False),
    }
