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
		Сhange = types.KeyboardButton("🔁 Сменить имя")
		Share = types.KeyboardButton("📢 Поделиться с друзьями")

		# Добавление кнопок в меню.
		Menu.add(Dose, Share, Сhange, row_width = 2)
		
		return Menu
