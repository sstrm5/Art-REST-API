from django.http import HttpRequest
from core.api.filters import PaginationIn, PaginationOut
from core.api.v1.questions.filters import (
    TestFilters,
    QuestionFilters,
    )
from core.apps.questions.exceptions.questions import CreateException
from core.apps.questions.services.questions import (
    BaseTestService,
    BaseQuestionService,
    ORMTestService,
    ORMQuestionService,
    )
from ninja import Query, Router
from ninja.errors import HttpError
from core.api.schemas import ApiResponse, ListPaginatedResponse, ListResponse
from core.api.v1.questions.schemas import (
    QuestionDataSchemaIn,
    TestAndQuestionDataSchemaIn,
    TestDataSchemaIn,
    TestSchemaIn,
    TestSchemaOut,
    QuestionSchemaOut,
    )


router = Router(tags=['Tests'])

@router.get('', response=ApiResponse)
def get_test_list_handler(
    request: HttpRequest,
    filters: Query[TestFilters], 
    pagination_in: Query[PaginationIn],
) -> ApiResponse:
    service: BaseTestService = ORMTestService()
    test_list = service.get_test_list(filters=filters, pagination=pagination_in)
    test_count = service.get_test_count(filters=filters)
    items = [TestSchemaOut.from_entity(obj) for obj in test_list]
    pagination_out = PaginationOut(
        offset=pagination_in.offset,
        limit=pagination_in.limit,
        total=test_count,
    )

    return ApiResponse(data=ListPaginatedResponse(items=items, pagination=pagination_out))


@router.get('/{test_id}', response=ApiResponse)
def get_test_handler(request, test_id: int) -> ApiResponse:
    service: BaseQuestionService = ORMQuestionService()
    question_list = service.get_question_list(test_id=test_id)
    # question_count = service.get_question_count(test_id=test_id)
    items = [QuestionSchemaOut.from_entity(obj) for obj in question_list]
    
    return ApiResponse(data=ListResponse(items=items))


@router.post('/create/new_test', response=ApiResponse)
def create_test_handler(
    request,
    payload: TestSchemaIn,
    ) -> ApiResponse:
    try:
        service: BaseTestService = ORMTestService()
        test = service.create_test(data=payload)
        test_schema = TestSchemaOut.from_entity(test)
        return ApiResponse(data=test_schema)
    except CreateException as exception:
        raise HttpError(status_code=400, message=exception.message)


@router.post('/check/test', response=ApiResponse)
def create_test_handler(
    request,
    payload: TestSchemaIn,
    ) -> ApiResponse:
    try:
        service: BaseTestService = ORMTestService()
        test = service.create_test(data=payload)
        test_schema = TestSchemaOut.from_entity(test)
        return ApiResponse(data=test_schema)
    except CreateException as exception:
        raise HttpError(status_code=400, message=exception.message)



@router.get('/hello_world')
def hello(request, name):
    return {'message': f'Hello, {name}!'}