from dublib.TelebotUtils import UserData
from telebot import types

class ReplyKeyboard:

	def __init__(self):
		pass

	def AddMenu(self, user: UserData) -> types.ReplyKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.ReplyKeyboardMarkup(resize_keyboard = True)

		# Генерация кнопок.
		Dose = types.KeyboardButton("💉 ДОЗА")
		List = types.KeyboardButton("⚙️ Настройки")
		Share = types.KeyboardButton("📢 Поделиться с друзьями")
		Write = types.KeyboardButton("💟 Написать послание")

		# Добавление кнопок в меню.
		Menu.add(Dose, Share, List, Write, row_width = 2)
		
		return Menu
