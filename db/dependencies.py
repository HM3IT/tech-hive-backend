from typing import Any
from litestar.di import Provide
from litestar import Request
from litestar.params import Parameter, Dependency
from uuid import UUID
from db.models import User as UserModel
from advanced_alchemy.filters import (
    BeforeAfter,
    CollectionFilter,
    LimitOffset,
    OrderBy,
    SearchFilter,
    FilterTypes,
)

__all__ = [
    "create_collection_dependencies",
    "provide_filter_dependencies",
    "provide_id_filter",
    "provide_limit_offset_pagination",
    "provide_search_filter",
    "BeforeAfter",
    "CollectionFilter",
    "LimitOffset",
    "OrderBy",
    "SearchFilter",
    "FilterTypes",
    "provide_user"
]

def provide_id_filter(
    ids: list[UUID] | None = Parameter(query="ids", default=None, required=False),
) -> CollectionFilter[UUID]:
    """Return type consumed by ``Repository.filter_in_collection()``.

    Args:
        ids (list[UUID] | None): Parsed out of a comma-separated list of values in query params.

    Returns:
        CollectionFilter[UUID]: Filter for a scoping query to a limited set of identities.
    """
    return CollectionFilter(field_name="id", values=ids or [])

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



async def provide_user(request: Request[UserModel, Any, Any]) -> UserModel:
    """Get the user from the connection.

    Args:
        request: current connection.

    Returns:
        User
    """
    return request.user


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

def provide_filter_dependencies(
    created_filter: BeforeAfter|None = Dependency(skip_validation=True),
    updated_filter: BeforeAfter|None  = Dependency(skip_validation=True),
    id_filter: CollectionFilter|None  = Dependency(skip_validation=True),
    limit_offset: LimitOffset |None = Dependency(skip_validation=True),
    search_filter: SearchFilter|None  = Dependency(skip_validation=True),
    order_by: OrderBy|None  = Dependency(skip_validation=True),
) -> list[FilterTypes]:
    filters: list[FilterTypes] = []
    if id_filter and id_filter.values:
        filters.append(id_filter)
    filters.extend(filter(None, [created_filter, limit_offset, updated_filter]))

    if search_filter and search_filter.field_name is not None and search_filter.value is not None:
        filters.append(search_filter)
    if order_by and order_by.field_name is not None:
        filters.append(order_by)
    return filters

def create_collection_dependencies() -> dict[str, Provide]:
    """Create ORM dependencies.

    Creates a dictionary of provides for pagination endpoints.
    Returns:
        dict[str, Provide]: Dictionary of provides for pagination endpoints.
    """ 
    return {
        "limit_offset": Provide(provide_limit_offset_pagination, sync_to_thread=False),
        "search_filter": Provide(provide_search_filter, sync_to_thread=False),
        "id_filter": Provide(provide_id_filter, sync_to_thread=False),
        "filters": Provide(provide_filter_dependencies, sync_to_thread=False),
    }
