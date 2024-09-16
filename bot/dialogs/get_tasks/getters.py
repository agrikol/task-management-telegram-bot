from aiogram_dialog import DialogManager
from aiogram.types import User
from bot.dialogs.create_task.getters import categories


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
    print(dialog_manager.dialog_data)
    categ = categories.get(dialog_manager.dialog_data.get("categ"), "Без категории")
    dialog_manager.dialog_data["categ"] = categ
    return dialog_manager.dialog_data


async def getter_of_categ(dialog_manager: DialogManager, **kwargs):
    return {"categories": [(value, key) for key, value in categories.items()]}
