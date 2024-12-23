from django.http import HttpRequest
from core.api.filters import PaginationIn
from core.api.v1.questions.filters import (
    TestFilters,
)
from core.apps.common.exceptions import ServiceException
from core.apps.customers.services.customers import BaseCustomerService
from core.apps.questions.containers import get_container
from core.apps.questions.services.attempts import BaseAttemptService
from core.apps.questions.services.questions import (
    BaseTestService,
    BaseQuestionService,
)
from core.apps.questions.use_cases import (
    CheckTestUseCase,
    CreateAttemptUseCase,
    CreateTestUseCase,
    GetAttemptListUseCase,
    GetSubjectsUseCase,
    GetTestUseCase,
)
from ninja import Query, Router, Header, File
from ninja.errors import HttpError
from ninja.files import UploadedFile
from core.api.schemas import ApiResponse, ListResponse
from core.api.v1.questions.schemas import (
    AnswersOut,
    AttemptSchemaIn,
    AttemptSchemaOut,
    AttemptSchemaOutWithName,
    AttemptUpdateSchema,
    TestAndQuestionDataSchemaIn,
    TestSchemaIn,
    TestSchemaOut,
    QuestionSchemaOut,
)


router = Router(tags=['Tests🚬'])


@router.get('', response=ApiResponse[ListResponse[TestSchemaOut]], summary='Получить список доступных тестов📜')
def get_test_list_handler(
    request: HttpRequest,
    filters: Query[TestFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse:

    container = get_container()
    service = container.resolve(BaseTestService)

    test_list = service.get_test_list(
        filters=filters, pagination=pagination_in)
    items = [TestSchemaOut.from_entity(obj) for obj in test_list]

    return ApiResponse(data=ListResponse(items=items))


@router.get('/{test_id}', response={200: ApiResponse[ListResponse[QuestionSchemaOut]]}, summary='Получить конкретный тест')
def get_test_handler(request, test_id: int) -> ApiResponse:

    container = get_container()
    use_case = GetTestUseCase(
        test_service=container.resolve(BaseTestService),
        question_service=container.resolve(BaseQuestionService),
    )

    try:
        question_list, test_duration = use_case.execute(test_id=test_id)
    except ServiceException as error:
        raise HttpError(status_code=400, message=error.message)

    items = [QuestionSchemaOut.from_entity(obj) for obj in question_list]

    return ApiResponse(data=ListResponse(items=items), meta={'duration': test_duration})


@router.post('/create/new_test', response={200: ApiResponse[TestSchemaOut]}, summary='Создать тест')
def create_test_handler(
    request,
    schema: TestSchemaIn,
    token: str = Header(alias='Auth-Token'),
    file: UploadedFile = File(alias='Image', required=False),
) -> ApiResponse:

    container = get_container()
    data: TestAndQuestionDataSchemaIn = schema.data
    use_case = CreateTestUseCase(
        test_service=container.resolve(BaseTestService),
        customer_service=container.resolve(BaseCustomerService)
    )

    try:
        test = use_case.execute(
            subject=data.test_info.subject,
            title=data.test_info.title,
            description=data.test_info.description,
            work_time=data.test_info.work_time,
            questions=data.questions,
            token=token,
            file=file,
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)
    return ApiResponse(data=TestSchemaOut.from_entity(test))


@router.post('/check/test', response=ApiResponse[AnswersOut], summary='Закончить попытку🍎')
def check_test_handler(
    request,
    schema: AttemptSchemaIn,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:

    container = get_container()

    use_case = CheckTestUseCase(
        customer_service=container.resolve(BaseCustomerService),
        test_service=container.resolve(BaseTestService),
        question_service=container.resolve(BaseQuestionService),
    )
    try:

        user_answers, correct_answers, total_score = use_case.execute(
            test_id=schema.test_id,
            token=token,
        )

    except Exception as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=AnswersOut(
        test_id=schema.test_id,
        user_answers=user_answers,
        correct_answers=correct_answers,
        total_score=total_score,
    ))


@router.post('/create/new_attempt', response=ApiResponse[AttemptSchemaOut], summary='Начать попытку🍏')
def create_attempt_handler(
    request,
    schema: AttemptSchemaIn,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:
    print(1232131231321312312313123123123)
    container = get_container()

    use_case = CreateAttemptUseCase(
        customer_service=container.resolve(BaseCustomerService),
        attempt_service=container.resolve(BaseAttemptService),
    )
    try:
        attempt = use_case.execute(
            token=token,
            test_id=schema.test_id,
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.post('/update/attempt', response=ApiResponse, summary='Обновить ответы на текущий тест➕')
def update_attempt_handler(
    request,
    schema: AttemptUpdateSchema,
    token: str = Header(alias='Auth-Token'),
) -> ApiResponse:
    container = get_container()
    service = container.resolve(BaseAttemptService)

    attempt = service.update_attempt(
        token=token,
        test_id=schema.test_id,
        user_answers=schema.user_answers,
    )

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.get('/{test_id}/attempts', response=ApiResponse[ListResponse[AttemptSchemaOutWithName]], summary='Получить список попыток на конкретный тест всех пользователей📜')
def get_attempt_list_handler(request, test_id: int) -> ApiResponse:
    container = get_container()

    use_case = GetAttemptListUseCase(
        attempt_service=container.resolve(BaseAttemptService),
        customer_service=container.resolve(BaseCustomerService),
    )
    try:
        attempt_list = use_case.execute(test_id=test_id)
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    items = [AttemptSchemaOutWithName(
        attempt_info=AttemptSchemaOut.from_entity(attempt_entity),
        user_name=user_name
    ) for attempt_entity, user_name in attempt_list]

    return ApiResponse(data=ListResponse(items=items))


@router.get('/subjects/get', response=ApiResponse[ListResponse])
def get_subjects_handler(request) -> ApiResponse:
    container = get_container()
    use_case = GetSubjectsUseCase(
        test_service=container.resolve(BaseTestService),
    )
    try:
        subjects = use_case.execute()
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)
    return ApiResponse(data=ListResponse(items=subjects))


@router.get('/hello_world/123')
def hello(request):
    return {'message': 'Hello!'}
