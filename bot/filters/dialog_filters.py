from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import BaseFilter
from aiogram_dialog.api.protocols.manager import Context


class DialogFilter(BaseFilter):
    def __init__(self, state: State):
        self.state = state

    async def __call__(self, _, aiogd_context: Context | None, **kwargs) -> bool:
        if aiogd_context is None:
            return False
        return self.state == aiogd_context.state.state


class DialogGroupFilter(BaseFilter):
    def __init__(self, states: StatesGroup):
        self.states = states

    async def __call__(self, _, aiogd_context: Context | None, **kwargs) -> bool:
        if aiogd_context is None:
            return False
        return self.states == aiogd_context.state.group
