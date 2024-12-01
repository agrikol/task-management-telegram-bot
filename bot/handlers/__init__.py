from .admin_command import admin_router
from .commands import commands_router
from .name_handler import task_name_router


routers = [admin_router, commands_router, task_name_router]
