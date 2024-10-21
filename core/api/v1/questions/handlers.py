from django.http import HttpRequest
from core.api.filters import PaginationIn, PaginationOut
from core.api.v1.questions.filters import (
    TestFilters,
    )
from core.apps.questions.entities.questions import AnswersOut
from core.apps.questions.exceptions.questions import CreateException
from core.apps.questions.services.attempts import BaseAttemptService, ORMAttemptService
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
    AnswersSchemaIn,
    AttemptSchemaIn,
    AttemptSchemaOut,
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
    items = [QuestionSchemaOut.from_entity(obj) for obj in question_list]
    
    return ApiResponse(data=ListResponse(items=items))


@router.post('/create/new_test', response=ApiResponse)
def create_test_handler(
    request,
    schema: TestSchemaIn,
    ) -> ApiResponse:
    try:
        service: BaseTestService = ORMTestService()
        test = service.create_test(data=schema)

        return ApiResponse(data=TestSchemaOut.from_entity(test))
    except CreateException as exception:
        raise HttpError(status_code=400, message=exception.message)


@router.post('/check/test', response=ApiResponse)
def check_test_handler(
    request,
    schema: AnswersSchemaIn,
    ) -> ApiResponse:
    try:
        test_service: BaseTestService = ORMTestService()
        question_service: BaseQuestionService = ORMQuestionService()
        questions = question_service.get_question_list(test_id=schema.test_id)
        test_id, user_answers, correct_answers, total_score = test_service.check_test(data=schema, questions=questions)

        return ApiResponse(data=AnswersOut(
            test_id=test_id,
            user_answers=user_answers,
            correct_answers=correct_answers,
            total_score=total_score,
        ))
    except Exception as exception:
        raise HttpError(status_code=400, message=exception.message)


@router.post('/create/new_attempt', response=ApiResponse)
def create_attempt_handler(
    request,
    schema: AttemptSchemaIn,
    ) -> ApiResponse:
        service: BaseAttemptService = ORMAttemptService()
        attempt = service.create_attempt(
            user_id=schema.user_id,
            test_id=schema.test_id,
            start_time=schema.start_time,
            end_time=schema.end_time,
            user_answers=schema.user_answers,
            total_score=schema.total_score,
        )

        return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.get('/{test_id}/attempts', response=ApiResponse)
def get_test_handler(request, test_id: int) -> ApiResponse:
    service: BaseAttemptService = ORMAttemptService()
    attempt_list = service.get_attempt_list(test_id=test_id)
    items = [AttemptSchemaOut.from_entity(obj) for obj in attempt_list]
    
    return ApiResponse(data=ListResponse(items=items))


@router.get('/hello_world')
def hello(request, name):
    return {'message': f'Hello, {name}!'}