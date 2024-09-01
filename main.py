from Source.InlineKeyboards import InlineKeyboards
from Source.ReplyKeyboard import ReplyKeyboard
from Source.Instruments import SendButtonDose
from Source.Reader import Reader
from Source.Thread import Reminder
from Source.AdminPanel import Panel
from Source.Moderator import Moderator

from dublib.Methods.JSON import ReadJSON, WriteJSON
from dublib.Methods.System import CheckPythonMinimalVersion, Clear
from dublib.Methods.Filesystem import MakeRootDirectories
from dublib.TelebotUtils import UsersManager
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

import telebot
import logging
import random
import os

Settings = ReadJSON("Settings.json")

logging.basicConfig(level=logging.INFO, encoding="utf-8", filename="LOGING.log", filemode="w",
	format='%(asctime)s - %(levelname)s - %(message)s',
	datefmt='%Y-%m-%d %H:%M:%S')

# Проверка поддержки используемой версии Python.
CheckPythonMinimalVersion(3, 10)

# Создание папок в корневой директории.
MakeRootDirectories(["Data/Users"])
MakeRootDirectories(["Data/Moderation"])

if os.path.exists("Data/Moderation/Moderation.json"): pass
else: 
	DefaultJson = {}
	WriteJSON("Data/Moderation/Moderation.json", DefaultJson)

# Очистка консоли.
Clear()

Bot = telebot.TeleBot(Settings["token"])
Manager = UsersManager("Data/Users")
InlineKeyboardsBox = InlineKeyboards()
ReplyKeyboardBox = ReplyKeyboard()
reader = Reader(Settings)
scheduler = BackgroundScheduler()
reminder = Reminder(Bot, Manager, Settings, reader, scheduler)
AdminPanel = Panel()

#==========================================================================================#
# >>>>> НАСТРОЙКИ APSHEDULER <<<<< #
#==========================================================================================#

StartDailyDose = Settings["start_dailydose"]

#==========================================================================================#
# >>>>> ДОБАВЛЕНИЕ ЗАДАНИЙ В APSHEDULER <<<<< #
#==========================================================================================#

job = scheduler.add_job(func=reminder.StartDailyDose, trigger='cron', hour = StartDailyDose["hour"], minute=StartDailyDose["minute"], id = 'job_1')
scheduler.start()

AdminPanel.decorators.commands(Bot, Manager, Settings["password"])

@Bot.message_handler(commands=["start"])
def ProcessCommandStart(Message: types.Message):
	User = Manager.auth(Message.from_user)
	User.set_property("Active", True)
	User.set_expected_type(None)
	Bot.send_message(
		Message.chat.id, 
		"Ну привет! ✌️\n\nА я знал, что тебя тоже ко мне занесёт.\nДавай-ка поднимем тебе самооценочку!"
		)
	try:
		call = User.get_property("Name")
		Bot.send_message(
			Message.chat.id, 
			f"{call}, мы рады видеть вас снова! 🤗",
			reply_markup= ReplyKeyboardBox.AddMenu(User)
			)
		
	except KeyError:
		Bot.send_message(
		Message.chat.id, 
		"Как тебя зовут?"
		)
		User.set_expected_type("Name")
	
AdminPanel.decorators.reply_keyboards(Bot, Manager)

@Bot.message_handler(content_types = ["text"], regexp = "📢 Поделиться с друзьями")
def ProcessShareWithFriends(Message: types.Message):
	User = Manager.auth(Message.from_user)

	Bot.send_photo(
		Message.chat.id, 
		photo = Settings["qr_id"],
		caption='@Ddoza_bot\n@Ddoza_bot\n@Ddoza_bot\n\nБот взаимной поддержки и повышения самооценки! 😎', 
		reply_markup=InlineKeyboardsBox.AddShare()
		)

@Bot.message_handler(content_types = ["text"], regexp = "💉 ДОЗА")
def ProcessDose(Message: types.Message):
	dose = None
	User = Manager.auth(Message.from_user)
	if User.get_property("Gender") =="Women":
		dose = reader.GetWD
	if User.get_property("Gender") =="Men":
		dose = reader.GetMD
	
	random_sentence = random.randint(1, len(dose))

	for Index in range(len(dose)):
		if Index == random_sentence-1:
			Bot.send_message(
				Message.chat.id,
				text = dose[Index]
				)

@Bot.message_handler(content_types = ["text"], regexp = "⚙️ Настройки")
def ProcessChangeName(Message: types.Message):
	User = Manager.auth(Message.from_user)
	Bot.send_message(
		Message.chat.id, 
		"Выберите пункт, который вы хотите настроить:", reply_markup= InlineKeyboardsBox.SettingsMenu())
	
@Bot.message_handler(content_types = ["text"], regexp = "💟 Написать послание")
def ProcessWrite(Message: types.Message):
	User = Manager.auth(Message.from_user)
	Bot.send_message(
		Message.chat.id, 
		"Выберите для кого вы хотите написать послание:", reply_markup= InlineKeyboardsBox.WriteFor())

@Bot.message_handler(content_types=["text"])
def ProcessText(Message: types.Message):
	User = Manager.auth(Message.from_user)
	if AdminPanel.procedures.text(Bot, User, Message): return

	if User.expected_type == "Name":
		User.set_property("Name", Message.text)
		User.set_expected_type(None)
		CallName = User.get_property("Name")
		
		try: 
			if User.get_property("Change"):
				Bot.send_message(
				Message.chat.id,
				f"Приятно познакомиться, {CallName}!")
				Bot.send_message(
				Message.chat.id,
				"Я надеюсь пол ты не сменил? 🤭\n\nА ну-ка укажи на всякий случай.\nА то я уже сомневаюсь!)",
				reply_markup= InlineKeyboardsBox.SelectionGender()
				)
		except:
			Bot.send_message(
				Message.chat.id,
				f"Уже неплохо, {CallName}! 😎\nДостойное имя!")
			Bot.send_message(
				Message.chat.id,
				"А ты кто вообще?", reply_markup= InlineKeyboardsBox.SelectionGender()
				)
	
	if User.expected_type == "Letter":
		text = Message.text

		if len(Message.text) > 200:
			Bot.send_message(
			Message.chat.id,
			"Превышение лимита, пожалуйста, повторите попытку"
			)
		else:
			User.set_temp_property("Moderation", Message.text)
			User.set_expected_type(None)
			Bot.send_message(
				Message.chat.id,
				f"Проверь, пожалуйста, все ли в норме?\nЕсли да, то нажми на \"Подтвердить\"\n\n{Message.text}",
				reply_markup= InlineKeyboardsBox.CheckLetter()
				)

AdminPanel.decorators.inline_keyboards(Bot, Manager)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Return"))
def ProcessWithoutReminders(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	Bot.delete_message(Call.message.chat.id, Call.message.id)
	
	Bot.answer_callback_query(Call.id)	

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Men"))
def ProcessMen(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	User.set_property("Gender", "Men")
	Bot.send_message(
		Call.message.chat.id, 
		"Я так и понял, что тут самец!)",
		reply_markup=ReplyKeyboardBox.AddMenu(User)
		)
	try:
		if User.get_property("Change"):
			User.clear_temp_properties()
	except:
		SendButtonDose(User, Bot, Call, InlineKeyboardsBox)
	
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Women"))
def ProcessWomen(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	User.set_property("Gender","Women")
	Bot.send_message(
		Call.message.chat.id, 
		"Уфф, а я чувствовал, что пахнет самочкой)", 
		reply_markup=ReplyKeyboardBox.AddMenu(User)
		)
	try:
		if User.get_property("Change"):
			User.clear_temp_properties()
	except:
		SendButtonDose(User, Bot, Call, InlineKeyboardsBox)

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("GirlFriend"))
def ProcessWomen(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)

	Bot.send_message(
			Call.message.chat.id, 
			"Отличный выбор\\! Кому\\-то из дам при нажатии на кнопку *\"ДОЗА\"* крупно повезет\\! А может и тебе\\)\nНапиши сообщение, которое ты хочешь пустить в широкие массы 😄\nУ тебя лимит на 200 символов\\.", 
			reply_markup=ReplyKeyboardBox.AddMenu(User),
			parse_mode= "MarkdownV2"
	)
	User.set_temp_property("WriteFor", "Women")
	User.set_expected_type("Letter")

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("BoyFriend"))
def ProcessMen(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)

	Bot.send_message(
			Call.message.chat.id, 
			"Отличный выбор\\! Кому\\-то из кавалеров при нажатии на кнопку *\"ДОЗА\"* крупно повезет\\! А может и тебе\\)\nНапиши сообщение, которое ты хочешь пустить в широкие массы 😄\nУ тебя лимит на 200 символов\\.", 
			reply_markup=ReplyKeyboardBox.AddMenu(User),
			parse_mode= "MarkdownV2"
			)
	User.set_temp_property("WriteFor", "Men")
	User.set_expected_type("Letter")

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Edit"))
def ProcessEdit(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	try:
		if User.get_property("Moderation"):
			Bot.send_message(
					Call.message.chat.id, 
					"Пожалуйста, отправьте исправленный текст."
					)
			User.set_expected_type("Letter")
	except: Bot.send_message(
			Call.message.chat.id, 
			"Вы отправили пустое сообщение."
			)
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Send"))
def ProcessSend(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)

	try: 
		Moderator().SaveUserSentences(User.get_property("Moderation"), User.get_property("WriteFor"))
		Bot.send_message(
				Call.message.chat.id, 
				"Супер! Текст принят!\nМодерация занимает от 1 до 2 недель.\nСкоро твоё послание увидит большой мир! 😉"
				)
	except: Bot.send_message(
			Call.message.chat.id, 
			"Вы отправили пустое сообщение."
			)
	User.clear_temp_properties()

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Dose"))
def ProcessDose(Call: types.CallbackQuery):
	dose = None
	User = Manager.auth(Call.from_user)
	if User.get_property("Gender") =="Women":
		dose = reader.GetWD
	if User.get_property("Gender") =="Men":
		dose = reader.GetMD
	
	random_sentence = random.randint(1, len(dose))

	for Index in range(len(dose)):
		if Index == random_sentence-1:
			Bot.send_message(
				Call.message.chat.id,
				text = dose[Index]
				)
			
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Change"))
def ProcessChangeName(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	User.set_expected_type("Name")
	Bot.send_message(
			Call.message.chat.id, 
			"Ну и как мне теперь тебя называть?")
	User.set_temp_property("Change", True)

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Info"))
def ProcessInfo(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)

	Bot.send_message(
		Call.message.chat.id,
		text = "@Ddoza\\_bot предназначен для поднятия настроения и повышения самооценки\\!\n\nБот ежедневно отправляет вам сообщения в рандомное время, имитируя общение живого человека, лучшего друга, и персонажа, который искренне вами дорожит\\! 😊\n\nВы можете дополнить послания бота нажав на кнопку \"Написать послание\"\\. Оно способно поддержать или согреть душу другого человека\\. Все новые послания проверяются модераторами и вводятся в работу\\! 💪\n\n_*Пользуйтесь, и не забывайте делиться с друзьями\\!*_",
		parse_mode= "MarkdownV2"
	)

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Settings_daily"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	
	Bot.send_message(
			Call.message.chat.id, 
			"Выберите режим входящих сообщений:",
			reply_markup=InlineKeyboardsBox.SettingsDaily())
	
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Deactivate"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	
	Bot.send_message(
			Call.message.chat.id, 
			"Эх ты.. А я думал мы друзья! 🥺\nНу ладно. Включить сообщения ты можешь в любой момент!",
			reply_markup=InlineKeyboardsBox.Sorry())
	
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Activate"))
def ProcessSettingsDaily(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	
	Bot.send_message(
			Call.message.chat.id, 
			"Я рад, что мы снова вместе! ❤️ 😉\nЗададим теперь жару!!!",
			reply_markup=InlineKeyboardsBox.Good())
	
	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Sorry"))
def ProcessSorry(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	Bot.delete_message(Call.message.chat.id, Call.message.id)
	User.set_property("Active", False)
	Bot.send_message(
			Call.message.chat.id, 
			"Ежедневная доза отключена!")

	Bot.answer_callback_query(Call.id)

@Bot.callback_query_handler(func = lambda Callback: Callback.data.startswith("Good"))
def ProcessGood(Call: types.CallbackQuery):
	User = Manager.auth(Call.from_user)
	Bot.delete_message(Call.message.chat.id, Call.message.id)
	User.set_property("Active", True)
	Bot.send_message(
			Call.message.chat.id, 
			"Ежедневная доза включена!")

	Bot.answer_callback_query(Call.id)

@Bot.message_handler(content_types = ["audio", "document", "video"])
def File(Message: types.Message):
	User = Manager.auth(Message.from_user)
	AdminPanel.procedures.files(Bot, User, Message)

AdminPanel.decorators.photo(Bot, Manager)

Bot.infinity_polling()

