from .start.dialogs import start_dialog
from .admin.dialogs import admin_dialog
from .create_task.dialogs import create_task_dialog
from .get_tasks.dialogs import task_list_dialog
from .feedback.dialogs import feedback_dialog
from .notification.dialog import notice_edit_dialog

dialogs = [
    start_dialog,
    admin_dialog,
    create_task_dialog,
    task_list_dialog,
    feedback_dialog,
    notice_edit_dialog,
]
