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
from core.apps.questions.services.test_sessions import BaseTestSessionService
from core.apps.questions.use_cases import (
    CreateAttemptUseCase,
    CreateTestUseCase,
    EndAttemptUseCase,
    GetAttemptInfoUseCase,
    GetAttemptListByCustomerUseCase,
    GetAttemptListUseCase,
    GetCurrentTestUseCase,
    GetLastAttemptResultUseCase,
    GetSubjectsUseCase,
    GetTestUseCase,
    UpdateAttemptAnswersUseCase,
)
from ninja import Query, Router, Header, File
from ninja.errors import HttpError
from ninja.files import UploadedFile
from core.api.schemas import ApiResponse, ListResponse
from core.api.v1.questions.schemas import (
    AnswersOut,
    AttemptIDSchema,
    AttemptInfoSchema,
    AttemptSchemaIn,
    AttemptSchemaOut,
    AttemptSchemaOutWithName,
    AttemptUpdateSchema,
    CurrentTestIdSchema,
    LastAttemptResultSchema,
    TestAndQuestionDataSchemaIn,
    TestSchemaIn,
    TestSchemaOut,
    QuestionSchemaOut,
)


router = Router(tags=["Tests🚬"])


@router.get(
    "",
    response=ApiResponse[ListResponse[TestSchemaOut]],
    summary="Получить список доступных тестов📜",
)
def get_test_list_handler(
    request: HttpRequest,
    filters: Query[TestFilters],
    pagination_in: Query[PaginationIn],
) -> ApiResponse:

    container = get_container()
    service = container.resolve(BaseTestService)

    test_list = service.get_test_list(filters=filters, pagination=pagination_in)
    items = [TestSchemaOut.from_entity(obj) for obj in test_list]

    return ApiResponse(data=ListResponse(items=items))


@router.get(
    "/{test_id}",
    response={200: ApiResponse[ListResponse[QuestionSchemaOut]]},
    summary="Получить конкретный тест",
)
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

    return ApiResponse(data=ListResponse(items=items), meta={"duration": test_duration})


@router.post(
    "/attempt/create",
    response=ApiResponse[AttemptSchemaOut],
    summary="Начать попытку🍏",
)
def create_attempt_handler(
    request,
    schema: AttemptSchemaIn,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse:
    container = get_container()

    use_case = CreateAttemptUseCase(
        customer_service=container.resolve(BaseCustomerService),
        attempt_service=container.resolve(BaseAttemptService),
        test_session_service=container.resolve(BaseTestSessionService),
        test_service=container.resolve(BaseTestService),
    )
    try:
        attempt = use_case.execute(
            token=token,
            test_id=schema.test_id,
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.post(
    "/attempt/update", response=ApiResponse, summary="Обновить ответы на текущий тест➕"
)
def update_attempt_handler(
    request,
    schema: AttemptUpdateSchema,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse:

    container = get_container()
    use_case = UpdateAttemptAnswersUseCase(
        customer_service=container.resolve(BaseCustomerService),
        attempt_service=container.resolve(BaseAttemptService),
        test_session_service=container.resolve(BaseTestSessionService),
    )
    try:
        attempt = use_case.execute(
            user_answers=schema.user_answers,
            token=token,
            test_id=schema.test_id,
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=AttemptSchemaOut.from_entity(entity=attempt))


@router.post("/attempt/end", response=ApiResponse, summary="Закончить попытку🍎")
def end_attempt_handler(
    request,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse:

    container = get_container()

    use_case = EndAttemptUseCase(
        customer_service=container.resolve(BaseCustomerService),
        test_service=container.resolve(BaseTestService),
        question_service=container.resolve(BaseQuestionService),
        test_session_service=container.resolve(BaseTestSessionService),
        attempt_service=container.resolve(BaseAttemptService),
    )

    try:
        test_id = use_case.execute(
            token=token,
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data={"test_id": test_id})


@router.post(
    "/attempt/result",
    response=ApiResponse,
    summary="Получить результаты последней попытки🍎",
)
def get_last_result_handler(
    request,
    token: str = Header(alias="Auth-Token"),
):
    container = get_container()

    use_case = GetLastAttemptResultUseCase(
        customer_service=container.resolve(BaseCustomerService),
        question_service=container.resolve(BaseQuestionService),
        attempt_service=container.resolve(BaseAttemptService),
        test_session_service=container.resolve(BaseTestSessionService),
        test_service=container.resolve(BaseTestService),
    )

    try:
        test_id, question_list, correct_answers, user_answers, total_score = (
            use_case.execute(
                token=token,
                device_info=request.META["HTTP_USER_AGENT"],
            )
        )
        question_list = [
            QuestionSchemaOut.from_entity(entity) for entity in question_list
        ]
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(
        data=LastAttemptResultSchema(
            test_id=test_id,
            question_list=question_list,
            correct_answers=correct_answers,
            user_answers=user_answers,
            total_score=total_score,
        )
    )


@router.post("/attempt/info", response={200: ApiResponse[AttemptInfoSchema]})
def get_info_about_attempt(
    request,
    schema: AttemptIDSchema,
    token: str = Header(alias="Auth-Token"),
):
    container = get_container()
    use_case = GetAttemptInfoUseCase(
        attempt_service=container.resolve(BaseAttemptService),
        customer_service=container.resolve(BaseCustomerService),
        test_service=container.resolve(BaseTestService),
        question_service=container.resolve(BaseQuestionService),
    )
    try:
        # сущность попытки с включенной информацией о вопросах, кол-ве вопросов, правильных овтетов
        attempt = use_case.execute(
            attempt_id=schema.attempt_id,
            token=token,
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    return ApiResponse(data=AttemptInfoSchema.from_entity(attempt))


@router.get(
    "/{test_id}/attempts",
    response=ApiResponse[ListResponse[AttemptSchemaOutWithName]],
    summary="Получить список попыток всех пользователей на конкретный тест📜",
)
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

    items = [
        AttemptSchemaOutWithName(
            attempt_info=AttemptSchemaOut.from_entity(attempt_entity),
            user_name=user_name,
        )
        for attempt_entity, user_name in attempt_list
    ]

    return ApiResponse(data=ListResponse(items=items))


@router.get(
    "/{test_id}/attempts/user",
    response=ApiResponse[ListResponse[AttemptSchemaOut]],
    summary="Получить список попыток ПОЛЬЗОВАТЕЛЯ на конкретный тест📜",
)
def get_attempt_list_handler_by_customer(
    request,
    test_id: int,
    token: str = Header(alias="Auth-Token"),
) -> ApiResponse:
    container = get_container()

    use_case = GetAttemptListByCustomerUseCase(
        attempt_service=container.resolve(BaseAttemptService),
        customer_service=container.resolve(BaseCustomerService),
    )
    try:
        attempt_list = use_case.execute(test_id=test_id, token=token)
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)

    items = [
        AttemptSchemaOut.from_entity(attempt_entity) for attempt_entity in attempt_list
    ]

    return ApiResponse(data=ListResponse(items=items))


@router.get(
    "/subjects/get", response=ApiResponse[ListResponse], summary="Получить список тем📜"
)
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


@router.get(
    "/test_session/get_test_id",
    response=ApiResponse[CurrentTestIdSchema],
    summary="Получить ID теста, который сейчас проходит пользователь",
)
def get_current_session_test_id(
    request,
    token: str = Header(alias="Auth-Token"),
):
    container = get_container()
    use_case = GetCurrentTestUseCase(
        test_session_service=container.resolve(BaseTestSessionService),
        customer_service=container.resolve(BaseCustomerService),
    )
    try:
        test_id, start_time, duration = use_case.execute(
            token=token,
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)
    return ApiResponse(
        data=CurrentTestIdSchema(
            test_id=test_id, start_time=start_time, duration=duration
        )
    )


@router.post(
    "/new_test/create",
    response={200: ApiResponse[TestSchemaOut]},
    summary="Создать тест",
)
def create_test_handler(
    request,
    schema: TestSchemaIn,
    token: str = Header(alias="Auth-Token"),
    file: UploadedFile = File(alias="Image", required=False),
) -> ApiResponse:

    container = get_container()
    data: TestAndQuestionDataSchemaIn = schema.data
    use_case = CreateTestUseCase(
        test_service=container.resolve(BaseTestService),
        customer_service=container.resolve(BaseCustomerService),
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
            device_info=request.META["HTTP_USER_AGENT"],
        )
    except ServiceException as exception:
        raise HttpError(status_code=400, message=exception.message)
    return ApiResponse(data=TestSchemaOut.from_entity(test))


@router.get("/hello_world/123")
def hello(request):
    return {"message": "Hello!"}
