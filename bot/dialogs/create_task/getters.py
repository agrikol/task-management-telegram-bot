from aiogram_dialog import DialogManager
import datetime


categories: dict = {
    "category_1": "🔴 Красная",
    "category_2": "🟡 Желтая",
    "category_3": "🟢 Зеленая",
    "category_4": "🔵 Синяя",
}


async def get_name(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    name = dialog_manager.dialog_data.get("name") or "<b>Новая</b>"
    desc = dialog_manager.dialog_data.get("desc") or "<i>Отсутствует</i>"
    due = dialog_manager.dialog_data.get("due") or datetime.date.today().strftime(
        "%d.%m.%Y"
    )
    categ = categories.get(dialog_manager.dialog_data.get("categ")) or "Без категории"
    notice = dialog_manager.dialog_data.get("notice") or "За 30 минут"
    return {"name": name, "desc": desc, "due": due, "categ": categ, "notice": notice}
