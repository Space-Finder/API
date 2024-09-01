__all__ = ("router_list", "middleware_list")

from .other import other_router
from .teacher import teacher_router
from .course import course_router
from .image import image_router
from .space import space_router
from .booking import booking_router

router_list = [
    other_router,
    teacher_router,
    course_router,
    image_router,
    space_router,
    booking_router,
]
middleware_list = []
