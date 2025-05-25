from typing import *
from uuid import UUID

import litestar
from litestar import Request, Response
from litestar.exceptions.http_exceptions import ClientException, NotFoundException
from litestar.params import Parameter

from api import schemas
from api.database import Database
from api.header import Header


class Controller(litestar.Controller):
    @litestar.get(
        "/",
        summary="List ingredients.",
        description=(
            "List ingredients in clients preferred language. "
            "Preferred language can be specified using the `Accept-Language` header or the `language` query parameter. "
            "Query parameter trumps header. "
            "If an ingredient does not exist in the client preferred language it will not be included in the listing. "
            "If `language` query parameter is set to original all ingredients will be included in the listing. "
            "Excluding both header and query parameter is the same as requesting original ingredients."
        ),
    )
    async def list(
        self,
        request: Request,
        language_code: str | None,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.Ingredient]]:
        async with Database() as client:
            result = await client.ingredients.list(language_code, limit, offset)
        return Response(
            [
                schemas.Ingredient.create(result.ingredient, result.translation)
                for result in result.results
            ],
            headers=Header.paging_links(request, limit, offset, result.count),
        )

    @litestar.get(
        "/{id:uuid}/languages",
        summary="List languages this ingredient is available in.",
    )
    async def list_languages(
        self,
        request: Request,
        id: UUID,
        limit: Annotated[int, Parameter(query="limit")] = 20,
        offset: Annotated[int, Parameter(query="offset")] = 0,
    ) -> Response[List[schemas.Language]]:
        async with Database() as client:
            result = await client.languages.list_by_ingredient(id, limit, offset)
        return Response(
            [schemas.Language.create(result.language) for result in result.results],
            headers=Header.paging_links(request, limit, offset, result.count),
        )

    @litestar.get(
        "/{id:uuid}/languages/{language_id:uuid}",
        summary="Fetch an ingredient in a specified language.",
    )
    async def fetch(
        self,
        request: Request,
        id: UUID,
        language_id: UUID,
    ) -> Response[schemas.Ingredient]:
        async with Database() as client:
            result = await client.ingredients.fetch_by_id(id, language_id)
            language_result = await client.languages.list_by_ingredient(
                result.ingredient.id
            )
        if not result:
            raise NotFoundException()
        return Response(
            schemas.Ingredient.create(result.ingredient, result.translation),
            headers=Header.last_modified(result.modified)
            | Header.translations_links(
                request,
                result.translation,
                [result.language for result in language_result.results],
            ),
        )

    @litestar.post(
        "/",
        summary="Create new ingredient.",
    )
    async def create(
        self, data: schemas.ingredient.IngredientCreatable
    ) -> Response[schemas.Ingredient]:
        async with Database() as client:
            result = await client.ingredients.create(data)
        return Response(
            schemas.Ingredient.create(result.ingredient, result.translation),
            headers=Header.last_modified(result.modified),
        )

    @litestar.put(
        "/{id:uuid}/languages/{language_id:uuid}",
        summary="Update a ingredients data and create or update the ingredients translation.",
        description=(
            "If the ingredient does not have a translation for the specified language a new translation will be created. "
            "If the translation does not exist the langauge specific data will be updated. "
            "Non langauge specific data is always updated."
        ),
    )
    async def change(
        self,
        id: UUID,
        language_id: UUID,
        data: schemas.Ingredient,
    ) -> Response[schemas.Ingredient]:
        if data.id != id or data.language_id != language_id:
            raise ClientException()
        async with Database() as client:
            result = await client.ingredients.update(id, data)
        return Response(
            schemas.Ingredient.create(result.ingredient, result.translation),
            headers=Header.last_modified(result.modified),
        )

    @litestar.delete(
        "/{id:uuid}",
        summary="Delete ingredient.",
        description="Delete all data related to this ingredient.",
    )
    async def delete(self, id: UUID) -> Response[None]:
        async with Database() as client:
            result = await client.ingredients.delete(id)
        if not result:
            raise NotFoundException()
        return Response(None)

    @litestar.delete(
        "/{id:uuid}/languages/{language_id:uuid}",
        summary="Delete translation for this ingredient.",
        description=(
            "Delete this translation for this ingredient. "
            "Can only be used if there is more than one translation."
        ),
    )
    async def delete_translation(self, id: UUID, language_id: UUID) -> Response[None]:
        async with Database() as client:
            result = await client.ingredients.delete_translation(id, language_id)
        if not result:
            raise ClientException(
                "Ingredient either does not exist or was not deleted due to it being the only translation."
            )
        return Response(None)
