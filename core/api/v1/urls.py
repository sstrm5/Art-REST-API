from ninja import Router

from core.api.v1.products.handlers import router as product_router
from core.api.v1.questions.handlers import router as question_router


router = Router(tags=['v1'])
router.add_router('products/', product_router)
router.add_router('questions/', question_router)
