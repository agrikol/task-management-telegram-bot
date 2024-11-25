from aiogram_dialog import DialogManager
from datetime import datetime
from aiogram.types import User
from bot.dialogs.create_task.getters import tags


async def getter_of_names(dialog_manager: DialogManager, **kwargs):
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(
            task_names=dialog_manager.start_data.get("task_names")
        )
        dialog_manager.start_data.clear()
    data = dialog_manager.dialog_data.get("task_names")
    return {"task_names": data}


async def getter_of_task(
    dialog_manager: DialogManager, event_from_user: User, **kwargs
):
    data = dialog_manager.dialog_data.copy()  # TODO: fix
    # if dialog_manager.start_data:
    #     data = dialog_manager.start_data
    data["tag"] = tags.get(data.get("tag"))
    data["due"] = f"{data['date']} {data['time']}".strip()
    data["is_time"] = data.get("time")
    data["notice"] = data.get("notice") or "Отсутствует"
    return data


async def getter_of_tag(dialog_manager: DialogManager, **kwargs):
    return {"tags": [(value, key) for key, value in tags.items()]}
