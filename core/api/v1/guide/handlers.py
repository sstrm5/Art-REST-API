from ninja import router
from ninja.errors import HttpError
from core.api.schemas import ApiResponse, ListResponse
from core.api.v1.guide.schemas import GuideSchema
from core.apps.guide import containers
from core.apps.guide.services.guide import BaseCardService
from core.apps.guide.use_cases import GetDetailInfoGuideCard


router = router.Router(tags=['Guide cards📕'])


@router.get('', response=ApiResponse[ListResponse[GuideSchema]], summary='Получить список карточек📜')
def list_guide_cards_handler(request):
    container = containers.get_container()
    card_service = container.resolve(BaseCardService)

    cards = card_service.get_all_cards()
    items = [GuideSchema.from_entity(card) for card in cards]
    return ApiResponse(data=ListResponse(items=items))


@router.get('/{id}', response=ApiResponse[GuideSchema], summary='Получить информацию о карточке')
def get_detail_guide_card(
    request,
    id: int,
):
    container = containers.get_container()
    # card_service = container.resolve(BaseCardService)
    use_case = GetDetailInfoGuideCard(
        card_service=container.resolve(BaseCardService),
    )

    try:
        card = use_case.execute(card_id=id)
    except Exception as exception:
        return HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=GuideSchema.from_entity(card))
