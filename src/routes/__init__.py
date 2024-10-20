__all__ = ("router_list", "middleware_list")

from .other import other_router
from .image import image_router

router_list = [other_router, image_router]
middleware_list = []
