from aiogram_dialog import DialogManager
from datetime import date, timedelta


tags: dict = {
    "0": "Без тэга",
    "1": "🔴",
    "2": "🟡",
    "3": "🟢",
    "4": "🔵",
}


async def get_template(
    dialog_manager: DialogManager,
    **kwargs,
) -> dict[str, str]:
    if dialog_manager.start_data:
        dialog_manager.dialog_data.update(dialog_manager.start_data)
        dialog_manager.start_data.clear()
    dialog_data = dialog_manager.dialog_data
    name = f"{dialog_data.setdefault('name', 'Новая')}"
    desc = f"{dialog_data.setdefault('desc', 'Отсутствует')}"
    _date = dialog_data.setdefault(
        "date", (date.today() + timedelta(days=1)).strftime("%d.%m.%Y")
    )
    _time = dialog_data.setdefault("time", "")
    tag = tags.get(dialog_data.setdefault("tag", "0"))
    notice: str | None = dialog_data.get("notice")
    notice = notice if notice else "Отсутствует"
    return {
        "name": name,
        "desc": desc,
        "due": f"{_date} {_time}",
        "tag": tag,
        "notice": notice,
        "is_time": _time != "",
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
            (hour + ":" + str(i).rjust(2, "0"), str(i).rjust(2, "0"))
            for i in range(0, 60, 5)
        ]
    }


async def getter_of_tag(dialog_manager: DialogManager, **kwargs):
    return {"tags": [(value, key) for key, value in tags.items()]}


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
