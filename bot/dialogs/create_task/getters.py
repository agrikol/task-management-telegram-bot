from aiogram_dialog import DialogManager
import datetime


async def get_name(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    name = dialog_manager.dialog_data.get("name") or "Новая"
    desc = dialog_manager.dialog_data.get("desc") or "Отсутствует"
    due = dialog_manager.dialog_data.get("due") or datetime.date.today().strftime(
        "%d.%m.%Y"
    )
    categ = dialog_manager.dialog_data.get("categ") or "Без категории"
    notice = dialog_manager.dialog_data.get("notice") or "За 30 минут"
    return {"name": name, "desc": desc, "due": due, "categ": categ, "notice": notice}
