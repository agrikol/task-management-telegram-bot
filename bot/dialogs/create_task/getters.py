from aiogram_dialog import DialogManager
from datetime import date, timedelta


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
    due = dialog_manager.dialog_data.get("due") or str(
        (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    )
    time = dialog_manager.dialog_data.get("time") or "12:00"
    categ = categories.get(dialog_manager.dialog_data.get("categ")) or "Без категории"
    notice = dialog_manager.dialog_data.get("notice") or "За 30 минут"
    return {
        "name": name,
        "desc": desc,
        "due": due + " " + time,
        "categ": categ,
        "notice": notice,
    }


async def get_hours(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    return {
        "time_list": [
            (str(i).rjust(2, "0") + ":", str(i).rjust(2, "0")) for i in range(0, 24)
        ]
    }


async def get_minutes(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    hour = dialog_manager.dialog_data.get("time")
    return {
        "time_list": [
            (hour + ":" + str(i).rjust(2, "0"), str(i)) for i in range(0, 60, 5)
        ]
    }


async def get_notice(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    return {
        "notice_list": [
            ("За минуту", "1"),
            ("За 5 минут", "5"),
            ("За 15 минут", "15"),
            ("За 30 минут", "30"),
            ("За час", "60"),
            ("За 3 часа", "180"),
            ("За 6 часов", "360"),
            ("За день", "1440"),
            ("За неделю", "10080"),
        ]
    }
