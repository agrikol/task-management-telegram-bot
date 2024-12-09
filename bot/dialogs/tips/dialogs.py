from operator import itemgetter
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.kbd import Button, Row, Select, Start, Back, Next, Cancel
from bot.states.states import TipsSG, LocationSG, StartSG
from bot.dialogs.start.getters import getter_of_start_data
from bot.dialogs.start.handlers import (
    start_create_task,
    start_get_tasks,
)


tips_dialog = Dialog(
    Window(
        Const("<b>Tip #1</b>"),
        Const(
            "Для того, чтобы сервис смог отправлять вам уведомления в корректное время - "
            "нужно указать часовой пояс, в котором вы находитесь."
        ),
        Start(Const("Указать часовой пояс"), id="timezone", state=LocationSG.MAIN),
        Row(
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
            Next(Const("Далее »"), id="next"),
        ),
        state=TipsSG.FIRST,
    ),
    Window(
        Const("<b>Tip #2</b>"),
        Const("Просмотрите короткий GIF, о способах создать задачу"),
        Row(
            Back(Const("« Назад"), id="back"),
            Start(Const("☰ Меню"), id="to_menu", state=StartSG.start),
            Next(Const("Далее »"), id="next"),
        ),
        state=TipsSG.SECOND,
    ),
)
# Window(
#     Format(
#         "🤖 Привет {name}, я - робот <b>MAKE-E</b>!\n"
#         "Перед началом настоятельно рекомендуем пройти короткий онбординг, "
#         "набрав команду /tips"
#     ),
#     Row(
#         Button(Const("Создать задачу"), id="new_task", on_click=start_create_task),
#         Button(
#             Const("Мои задачи"),
#             id="my_tasks",
#             on_click=start_get_tasks,
#             when="is_tasks",
#         ),
#     ),
#     Select(
#         Format("{item[0]}"),
#         id="today",
#         item_id_getter=itemgetter(1),
#         items="today_date",
#         on_click=start_get_tasks,
#         when="is_today",
#     ),
#     getter=getter_of_start_data,
#     state=StartSG.start,
# ),
