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
	
	def AddShare(self) -> types.InlineKeyboardMarkup:
		Menu = types.InlineKeyboardMarkup()

		Share = types.InlineKeyboardButton(
			"Поделиться", 
			switch_inline_query='\n\nБот взаимной поддержки и повышения самооценки! 😎'
			)
		
		Menu.add(Share)

		return Menu
	
	def SettingsMenu(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		SettingsDaily = types.InlineKeyboardButton("❎️ Вкл/выкл сообщения", callback_data = f"Settings_daily")
		Сhange = types.InlineKeyboardButton("🔄 Сменить имя", callback_data = f"Change")
		Info = types.InlineKeyboardButton("🔆 Инфа", callback_data = f"Info")
		Return = types.InlineKeyboardButton("🔙 Назад", callback_data = f"Return")
		# Добавление кнопок в меню.
		Menu.add(SettingsDaily, Сhange, Info, Return, row_width= 1) 

		return Menu

	def SettingsDaily(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Deactivate = types.InlineKeyboardButton("❌️ Отключить сообщения", callback_data = f"Deactivate")
		Activate = types.InlineKeyboardButton("✅️ Включить сообщения", callback_data = f"Activate")
		# Добавление кнопок в меню.
		Menu.add(Deactivate, Activate, row_width= 1) 

		return Menu

	def Sorry(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Sorry = types.InlineKeyboardButton("Прости! Но так будет лучше..", callback_data = f"Sorry")
		# Добавление кнопок в меню.
		Menu.add(Sorry, row_width= 1) 

		return Menu
	
	def Good(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Good = types.InlineKeyboardButton("Взаимно! Я тоже!)", callback_data = f"Good")
		# Добавление кнопок в меню.
		Menu.add(Good, row_width= 1) 

		return Menu

	
	def WriteFor(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		GirlFriend = types.InlineKeyboardButton("🧚‍♀️ Для девушки", callback_data = f"GirlFriend")
		BoyFriend = types.InlineKeyboardButton("🏋‍♂️ Для парня", callback_data = f"BoyFriend")

		# Добавление кнопок в меню.
		Menu.add(GirlFriend, BoyFriend, row_width= 1) 

		return Menu
	
	def CheckLetter(self) -> types.InlineKeyboardMarkup:
		# Кнопочное меню.
		Menu = types.InlineKeyboardMarkup()

		# Генерация кнопок.
		Send = types.InlineKeyboardButton("🟢 Подтвердить", callback_data = f"Send")
		Edit = types.InlineKeyboardButton("🔴 Переделать", callback_data = f"Edit")
		# Добавление кнопок в меню.
		Menu.add(Send, Edit, row_width= 1) 

		return Menu
	

