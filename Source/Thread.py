from .Reader import Reader
from .Instruments import ChoiceSentence

from apscheduler.schedulers.background import BackgroundScheduler
from dublib.TelebotUtils import UsersManager
from telebot import TeleBot

import  datetime
import os
import random
import logging

class Reminder:
	def __init__(self, bot: TeleBot, Manager: UsersManager, Settings: dict, reader: Reader, scheduler: BackgroundScheduler):
		self.__Bot = bot
		self.__Manager = Manager
		self.__Settings = Settings
		self.__reader = reader
		self.__scheduler = scheduler

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

	def StartDailyDose(self):
		UsersID = self.__GetUsersID()

		for ID in UsersID:

			User = self.__Manager.get_user(ID)
			if User.get_property("Active"):
				try:
					if User.get_property("Gender") == "Women":
						Sentence = ChoiceSentence(self.__reader.GetWR)
					if User.get_property("Gender") == "Men":
						Sentence = ChoiceSentence(self.__reader.GetMR)
				except: logging.info(f"Gender для {ID} отсутствует.")
				
				try:
					logging.info(f"Начата рассылка: {ID}, {Sentence}")
					CallName = User.get_property("Name")	
					self.__Bot.send_message(
						ID,
						text = f"{CallName}, {Sentence}"
						)
				except: User.set_chat_forbidden(True)
			else: pass
		Hour = random.randint(7, 20)
		Minute = random.randint(0, 59)
		today = datetime.datetime.today()
		HourNow = int(datetime.datetime.now().strftime("%H"))
		MinuteNow = int(datetime.datetime.now().strftime("%M"))
		tomorrow = today + datetime.timedelta(days=1)
		logging.info(f"Новое время {Hour}, {Minute}")
		if Hour > HourNow: self.__scheduler.reschedule_job(job_id='job_1', trigger='cron', start_date = tomorrow, hour =Hour, minute=Minute)
		if Hour == HourNow:
			if Minute> MinuteNow: self.__scheduler.reschedule_job(job_id='job_1', trigger='cron', start_date = tomorrow, hour =Hour, minute=Minute)
			if Minute == MinuteNow:self.__scheduler.reschedule_job(job_id='job_1', trigger='cron', start_date = tomorrow, hour =Hour, minute=Minute)
			if Minute < MinuteNow: self.__scheduler.reschedule_job(job_id='job_1', trigger='cron', start_date = today, hour =Hour, minute=Minute)
		if Hour < HourNow: self.__scheduler.reschedule_job(job_id='job_1', trigger='cron', start_date = today, hour =Hour, minute=Minute)
		

