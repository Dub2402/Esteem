from .Reader import Reader
from .Instruments import ChoiceSentence

from dublib.TelebotUtils import UsersManager
from dublib.Methods.JSON import WriteJSON
from dublib.Methods.JSON import ReadJSON
from telebot import TeleBot

import os
import random
import logging

class Reminder:
	def __init__(self, bot: TeleBot, Manager: UsersManager, Settings: dict, reader: Reader):
		self.__Bot = bot
		self.__Manager = Manager
		self.__Settings = Settings
		self.__reader = reader

	def __GetUsersID(self) -> list[int]:
		# Получение списка файлов в директории.
		Files = os.listdir("Data/Users")
		# Фильтрация только файлов формата JSON.
		Files = list(filter(lambda List: List.endswith(".json"), Files))
		# Список ID пользователей.
		UsersID = list()

		# Для каждого файла.
		for File in Files:
			# Получение ID пользователя.
			ID = int(File.replace(".json", ""))
			# Добавление ID в список.
			UsersID.append(ID)

		return UsersID
	
	def StartRandomaizer(self):
		Hour = random.randint(7, 20)
		Minute = random.randint(0, 59)
		self.__Settings["start_dailydose"]["hour"] = Hour
		self.__Settings["start_dailydose"]["minute"] = Minute
		WriteJSON("Settings.json", self.__Settings)

	def StartDailyDose(self):
		UsersID = self.__GetUsersID()

		for ID in UsersID:

			User = self.__Manager.get_user(ID)
			if User.get_property("Gender") =="W":
				Sentence = ChoiceSentence(self.__reader.GetWR)
			if User.get_property("Gender") =="M":
				Sentence = ChoiceSentence(self.__reader.GetMR)

			logging.info(f"Начата рассылка: {ID}, {Sentence} ")
			CallName = User.get_property("Name")
			try:	
				self.__Bot.send_message(
					ID,
					text = f"{CallName}, {Sentence}"
					)
			except: User.set_chat_forbidden(True)
