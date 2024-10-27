from django.http import HttpRequest
from django.urls import path
from django.conf.urls.static import static

# from core.project.settings import local
from django.conf import settings
from ninja import NinjaAPI

from core.api.schemas import PingResponseSchema
from core.api.v1.urls import router as v1_router


api = NinjaAPI()


@api.get("/ping", response=PingResponseSchema)
def ping(request: HttpRequest) -> PingResponseSchema:
    return PingResponseSchema(result=True)


api.add_router('v1/', v1_router)

urlpatterns = [
    path("", api.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
