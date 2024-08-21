from Source.InlineKeyboards import InlineKeyboards
from Source.ReplyKeyboard import ReplyKeyboard
from Source.Instruments import SendButtonDose
from Source.Reader import Reader
from Source.Thread import Reminder

from dublib.Methods.JSON import ReadJSON
from dublib.Methods.System import CheckPythonMinimalVersion, Clear
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.TelebotUtils import UsersManager
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

import telebot
import logging
import random

Settings = ReadJSON("Settings.json")

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 10)

# Создание папок в корневой директории.
MakeRootDirectories(["Data/Users"])
# Очистка консоли.
Clear()

Bot = telebot.TeleBot(Settings["token"])
Manager = UsersManager("Data/Users")
InlineKeyboardsBox = InlineKeyboards()
ReplyKeyboardBox = ReplyKeyboard()
reader = Reader(Settings)
scheduler = BackgroundScheduler()
reminder = Reminder(Bot, Manager, Settings, reader)

#==========================================================================================#
# >>>>> НАСТРОЙКИ APSHEDULER <<<<< #
#==========================================================================================#

StartRandom = Settings["start_random"]
StartDailyDose = Settings["start_dailydose"]

#==========================================================================================#
# >>>>> ДОБАВЛЕНИЕ ЗАДАНИЙ В APSHEDULER <<<<< #
#==========================================================================================#

scheduler.add_job(reminder.StartRandomaizer, 'cron', hour = StartRandom["hour"], minute=StartRandom["minute"])
scheduler.add_job(reminder.StartDailyDose, 'cron', hour = StartDailyDose["hour"], minute=StartDailyDose["minute"])
scheduler.start()

@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
	User = Manager.auth(Message.from_user)
	User.set_expected_type(None)
	Bot.send_message(
		Message.chat.id, 
		"Ну, привет!) ✌️\n\nА я знал, что тебя тоже ко мне занесёт! Что? Стало интересно, что это за штуковина. Тогда давай действовать! Поднимем тебе самооценочку! 😉😄"
		)
	Bot.send_message(
		Message.chat.id, 
		"Как ты говоришь тебя зовут?"
		)
	User.set_expected_type("Name")

@Bot.message_handler(content_types = ["text"], regexp = "📢 Поделиться с друзьями")
def ProcessShareWithFriends(Message: types.Message):
	User = Manager.auth(Message.from_user)
	pass

@Bot.message_handler(content_types = ["text"], regexp = "💉 ДОЗА")
def ProcessDose(Message: types.Message):
	dose = None
	User = Manager.auth(Message.from_user)
	if User.get_property("Gender") =="W":
		dose = reader.GetWD
	if User.get_property("Gender") =="M":
		dose = reader.GetMD
	
	random_sentence = random.randint(1, len(dose))

	for Index in range(len(dose)):
		if Index == random_sentence-1:
			Bot.send_message(
				Message.chat.id,
				text = dose[Index]
				)

@Bot.message_handler(content_types = ["text"], regexp = "🔁 Сменить имя")
def ProcessChangeName(Message: types.Message):
	User = Manager.auth(Message.from_user)
	pass

@Bot.message_handler(content_types=["text"])
def ProcessText(Message: types.Message):
	User = Manager.auth(Message.from_user)

	if User.expected_type == "Name":
		User.set_property("Name", Message.text)
		User.set_expected_type(None)
		Bot.send_message(
			Message.chat.id,
			"Нормально-нормально! 😎")
		Bot.send_message(
			Message.chat.id,
			"А ты вообще кто?", reply_markup= InlineKeyboardsBox.SelectionGender()
			)
			
@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Men"))
def ProcessTextNewReminder(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	User.set_property("Gender","M")
	
	Bot.send_message(
			Call.message.chat.id, 
			"А я так и понял, что это самец!)",
			reply_markup=ReplyKeyboardBox.AddMenu(User))
	SendButtonDose(User, Bot, Call, InlineKeyboardsBox)
	
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Women"))
def ProcessTextNewReminder(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	User.set_property("Gender","W")

	Bot.send_message(
			Call.message.chat.id, 
			"Уфф, а я чувствовал, что пахнет самочкой)", 
			reply_markup=ReplyKeyboardBox.AddMenu(User))
	SendButtonDose(User, Bot, Call, InlineKeyboardsBox)

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Dose"))
def ProcessTextNewReminder(Call: types.CallbackQuery):
	dose = None
	User = Manager.auth(Call.from_user)
	if User.get_property("Gender") =="W":
		dose = reader.GetWD
	if User.get_property("Gender") =="M":
		dose = reader.GetMD
	
	random_sentence = random.randint(1, len(dose))

	for Index in range(len(dose)):
		if Index == random_sentence-1:
			Bot.send_message(
				Call.message.chat.id,
				text = dose[Index]
				)
			
	Bot.answer_callback_query(Call.id)

Bot.infinity_polling()