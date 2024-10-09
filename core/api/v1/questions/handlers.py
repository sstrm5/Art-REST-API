from django.http import HttpRequest
from core.api.filters import PaginationIn, PaginationOut
from core.api.v1.questions.filters import (
    TestFilters,
    QuestionFilters,
    )
from core.apps.questions.services.questions import (
    BaseTestService,
    BaseQuestionService,
    ORMTestService,
    ORMQuestionService,
    )
from ninja import Query, Router
from core.api.schemas import ApiResponse, ListPaginatedResponse, ListResponse
from core.api.v1.questions.schemas import (
    TestSchema,
    QuestionSchema,
    )

router = Router(tags=['Tests'])

@router.get('', response=ApiResponse[ListPaginatedResponse[TestSchema]])
def get_test_list_handler(
    request: HttpRequest,
    filters: Query[TestFilters], 
    pagination_in: Query[PaginationIn],
) -> ApiResponse[ListPaginatedResponse[TestSchema]]:
    service: BaseTestService = ORMTestService()
    test_list = service.get_test_list(filters=filters, pagination=pagination_in)
    test_count = service.get_test_count(filters=filters)
    items = [TestSchema.from_entity(obj) for obj in test_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=test_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/{test_id}', response=ApiResponse[ListResponse[QuestionSchema]])
def get_test_handler(request, test_id: int) -> ApiResponse[QuestionSchema]:
    service: BaseQuestionService = ORMQuestionService()
    question_list = service.get_question_list(test_id=test_id)
    # question_count = service.get_question_count(test_id=test_id)
    items = [QuestionSchema.from_entity(obj) for obj in question_list]
    
    return ApiResponse(data=ListResponse(items=items))



@router.get('/hello_world')
def hello(request, name):
    return {'message': f'Hello, {name}!'}