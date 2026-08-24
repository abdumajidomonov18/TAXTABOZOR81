from aiogram.fsm.state import State, StatesGroup


class RegistrationStates(StatesGroup):
    waiting_for_contact = State()


class AddressStates(StatesGroup):
    waiting_for_location = State()
    waiting_for_title = State()


class OrderStates(StatesGroup):
    entering_name = State()
    selecting_address = State()
    selecting_payment = State()
    entering_comment = State()
    confirming = State()



class SearchStates(StatesGroup):
    waiting_for_query = State()


class ProductStates(StatesGroup):
    waiting_for_quantity = State()

