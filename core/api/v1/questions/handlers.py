from django.http import HttpRequest
from core.api.filters import PaginationIn, PaginationOut
from core.api.v1.questions.filters import QuestionFilters
from core.apps.questions.services.questions import BaseQuestionService, ORMQuestionService
from ninja import Query, Router
from core.api.schemas import ApiResponse, ListPaginatedResponse
from core.api.v1.questions.schemas import QuestionSchema

router = Router(tags=['Questions'])

@router.get('', response=ApiResponse[ListPaginatedResponse[QuestionSchema]])
def get_question_list_handler(
    request: HttpRequest,
    filters: Query[QuestionFilters], 
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[QuestionSchema]]:
    service: BaseQuestionService = ORMQuestionService()
    question_list = service.get_question_list(filters=filters, pagination=pagination_in)
    question_count = service.get_question_count(filters=filters)
    items = [QuestionSchema.from_entity(obj) for obj in question_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=question_count,
    )
    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/hello')
def hello(request, name):
    return {'message': f'Hello, {name}!'}