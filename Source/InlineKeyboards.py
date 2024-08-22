from dublib.TelebotUtils import UserData
from telebot import types

class InlineKeyboards:

	def __init__(self):
		pass

	def SelectionGender(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Women = types.InlineKeyboardButton("♀️ Женщина", callback_data = f"Women")
		Men = types.InlineKeyboardButton("️♂️ Мужчина", callback_data = f"Men")
		
		# Добавление кнопок в меню.
		Menu.add(Women, Men, row_width= 1) 

		return Menu
	
	def Dose(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Dose = types.InlineKeyboardButton("Доза", callback_data = f"Dose")
		
		# Добавление кнопок в меню.
		Menu.add(Dose, row_width= 1) 

		return Menu


