from __future__ import annotations

from uuid import UUID
from logging import getLogger

from litestar import get, post, patch
from litestar.di import Provide
from litestar.params import Parameter
from litestar.controller import Controller
from litestar.pagination import OffsetPagination
from litestar.repository.filters import LimitOffset

from domain.tags import urls
from domain.tags.services import TagService
from domain.tags.schemas import Tag, TagCreate
from domain.tags.depedencies import provide_tag_service

from domain.users.guards import requires_active_user, requires_superuser


logger = getLogger()

class TagController(Controller):
    
    """Tag CRUD"""
    tags = ["Tags"]
    dependencies = {"tag_service": Provide(provide_tag_service),}

    @get(path=urls.TAG_LIST)
    async def list_tag(
        self,
        tag_service: TagService,
        limit_offset: LimitOffset,
    ) -> OffsetPagination[Tag]:
        """List Tags."""
        results, total = await tag_service.list_and_count(limit_offset)
        filters = [limit_offset]
        return tag_service.to_schema(data=results, total=total, schema_type=Tag, filters=filters)

    @post(path=urls.TAG_ADD, guards=[requires_active_user, requires_superuser])
    async def create_tag(
        self,
        tag_service: TagService,
        data: TagCreate,
    ) -> Tag:
        """Create a new Tag."""
        tag = data.to_dict()
        tag_obj = await tag_service.create(tag)
        return tag_service.to_schema(data=tag_obj, schema_type=Tag)


    @get(path=urls.TAG_DETAIL)
    async def get_tag(
        self,
        tag_service: TagService,
        id: UUID = Parameter(
            title="Tag ID",
            description="The Tag to retrieve.",
        ),
    ) -> Tag:
        """Get an existing Tag."""
        tag_obj = await tag_service.get(item_id=id)
        return tag_service.to_schema(data=tag_obj,  schema_type=Tag)

    @patch(
        path=urls.TAG_UPDATE, guards=[requires_superuser, requires_active_user]
    )
    async def update_tag(
        self,
        tag_service: TagService,
        data: TagCreate,
        id: UUID = Parameter(
            title="Tag ID",
            description="The Tag to update.",
        ),
    ) -> Tag:
        """Update a Tag."""
        category = data.to_dict()
        tag_obj = await tag_service.update(item_id=id, data=category)
        return tag_service.to_schema(tag_obj, schema_type=Tag)