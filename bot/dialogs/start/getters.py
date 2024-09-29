from bot.config.version import VERSION, DATE
from datetime import date
from aiogram.types import User
from aiogram_dialog import DialogManager
from bot.db.requests import check_tasks_exist


# TEST_DATA = f"""\
# \n\n🚧 <b>Текущая версия бота: {VERSION} от {DATE}</b>.\n
# Это бета-версия бота и некоторые его функции могут быть \
# еще не реализованы или работать не так, как задумано. \
# Оставьте отзыв или сообщение об ошибке по команде /feedback, \
# это точно поможет в разработке.\n\n\
# Ближайшие обновления:\n- сортировка задач;\n- уведомления.\n\n\
# Не стесняйтесь эксплуатировать и ломать бота любыми возможными способами.\n\n
# Спасибо за участие 🤖
# """


async def getter_of_start_data(
    dialog_manager: DialogManager,
    event_from_user: User,
    **kwargs,
) -> dict[str, str | list[tuple[str, str]] | bool]:
    session = dialog_manager.middleware_data.get("session")
    today = date.today()
    formatted_date = today.strftime("Сегодня %d.%m")  # TODO: add locale
    tasks, today_tasks = await check_tasks_exist(session, event_from_user.id)
    return {
        "name": event_from_user.full_name or event_from_user.username,
        "today_date": [(formatted_date, str(today))],
        "is_tasks": tasks,
        "is_today": today_tasks,
        # "intro": TEST_DATA,
    }
