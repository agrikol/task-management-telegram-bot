from aiogram.fsm.state import State, StatesGroup


class StartSG(StatesGroup):
    start = State()


class NewTaskSG(StatesGroup):
    start = State()
    
    
class ShowTaskSG(StatesGroup):
    start = State()