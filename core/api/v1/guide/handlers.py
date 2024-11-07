from ninja import router

from core.api.schemas import ApiResponse, ListResponse
from core.api.v1.guide.schemas import GuideSchema
from core.apps.guide import containers
from core.apps.guide.services.guide import BaseCardService


router = router.Router(tags=['Guide cards'])


@router.get('', response=ApiResponse)
def list_guide_cards_handler(request):
    container = containers.get_container()
    card_service = container.resolve(BaseCardService)

    cards = card_service.get_all_cards()
    items = [GuideSchema.from_entity(card) for card in cards]
    return ApiResponse(data=ListResponse(items=items))
